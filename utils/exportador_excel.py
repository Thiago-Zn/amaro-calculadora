"""exportador_excel.py - exportação para Excel"""
import pandas as pd
import io
from datetime import datetime
import streamlit as st
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.chart import PieChart, BarChart, Reference
import base64

def create_excel_report(dados_simulacao, modelo, parametros, tipo_analise="Custo por Trecho"):
    """
    Cria um relatório Excel completo com múltiplas abas.
    
    Args:
        dados_simulacao (dict): Dados da simulação realizada
        modelo (str): Modelo da aeronave
        parametros (dict): Parâmetros utilizados na simulação
        tipo_analise (str): Tipo de análise realizada
    
    Returns:
        bytes: Conteúdo do Excel em bytes
    """
    
    # Create workbook
    wb = Workbook()
    
    # Remove default sheet
    wb.remove(wb.active)
    
    # Create sheets
    ws_resumo = wb.create_sheet("Resumo Executivo")
    ws_custos = wb.create_sheet("Detalhamento Custos")
    ws_comparativo = wb.create_sheet("Comparativo Mercado")
    ws_parametros = wb.create_sheet("Parâmetros")
    ws_dados = wb.create_sheet("Dados Brutos")
    
    # Styles
    header_font = Font(bold=True, size=14, color="FFFFFF")
    header_fill = PatternFill(start_color="8C1D40", end_color="8C1D40", fill_type="solid")
    subheader_font = Font(bold=True, size=12)
    border = Border(left=Side(style='thin'), right=Side(style='thin'), 
                   top=Side(style='thin'), bottom=Side(style='thin'))
    
    # === ABA 1: RESUMO EXECUTIVO ===
    ws_resumo.title = "Resumo Executivo"
    
    # Header
    ws_resumo['A1'] = "AMARO AVIATION - RELATÓRIO DE ANÁLISE"
    ws_resumo['A1'].font = Font(bold=True, size=16)
    ws_resumo.merge_cells('A1:D1')
    
    ws_resumo['A2'] = f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    ws_resumo['A3'] = f"Modelo: {modelo}"
    ws_resumo['A4'] = f"Tipo de Análise: {tipo_analise}"
    
    # Principais métricas
    row = 6
    ws_resumo[f'A{row}'] = "PRINCIPAIS RESULTADOS"
    ws_resumo[f'A{row}'].font = subheader_font
    row += 2
    
    if 'total' in dados_simulacao:
        custo_total = dados_simulacao['total']
        preco_mercado = parametros.get('preco_mercado_hora', {}).get(modelo, 0)
        economia = preco_mercado - custo_total if preco_mercado > custo_total else 0
        
        metricas = [
            ("Custo Operacional/hora", f"R$ {custo_total:,.2f}"),
            ("Preço Mercado/hora", f"R$ {preco_mercado:,.2f}"),
            ("Economia/hora", f"R$ {economia:,.2f}"),
            ("Percentual Economia", f"{(economia/preco_mercado*100):.1f}%" if preco_mercado > 0 else "0%")
        ]
        
        for i, (label, value) in enumerate(metricas):
            ws_resumo[f'A{row+i}'] = label
            ws_resumo[f'B{row+i}'] = value
            ws_resumo[f'A{row+i}'].font = Font(bold=True)
    
    # === ABA 2: DETALHAMENTO DE CUSTOS ===
    if all(key in dados_simulacao for key in ['preco_comb', 'manut', 'piloto', 'depr']):
        custos_df = pd.DataFrame({
            'Componente': ['Combustível', 'Manutenção', 'Piloto', 'Depreciação', 'TOTAL'],
            'Valor (R$)': [
                dados_simulacao['preco_comb'],
                dados_simulacao['manut'],
                dados_simulacao['piloto'],
                dados_simulacao['depr'],
                dados_simulacao['total']
            ],
            'Percentual (%)': [
                (dados_simulacao['preco_comb']/dados_simulacao['total']*100),
                (dados_simulacao['manut']/dados_simulacao['total']*100),
                (dados_simulacao['piloto']/dados_simulacao['total']*100),
                (dados_simulacao['depr']/dados_simulacao['total']*100),
                100.0
            ]
        })
        
        # Add dataframe to sheet
        for r in dataframe_to_rows(custos_df, index=False, header=True):
            ws_custos.append(r)
        
        # Format header
        for col in range(1, 4):
            cell = ws_custos.cell(row=1, column=col)
            cell.font = header_font
            cell.fill = header_fill
            cell.border = border
        
        # Format data rows
        for row in range(2, 7):
            for col in range(1, 4):
                cell = ws_custos.cell(row=row, column=col)
                cell.border = border
                if col == 2:  # Value column
                    cell.number_format = 'R$ #,##0.00'
                elif col == 3:  # Percentage column
                    cell.number_format = '0.0%'
        
        # Format total row
        for col in range(1, 4):
            cell = ws_custos.cell(row=6, column=col)
            cell.font = Font(bold=True)
            cell.fill = PatternFill(start_color="F0F2F6", end_color="F0F2F6", fill_type="solid")
    
    # === ABA 3: COMPARATIVO COM MERCADO ===
    modelos_disponiveis = list(parametros.get('consumo_modelos', {}).keys())
    comparativo_data = []
    
    for modelo_comp in modelos_disponiveis:
        consumo = parametros.get('consumo_modelos', {}).get(modelo_comp, 0)
        custo_combustivel = consumo * parametros.get('preco_combustivel', 0)
        custo_manutencao = parametros.get('custo_manutencao', {}).get(modelo_comp, 0)
        custo_piloto = parametros.get('custo_piloto_hora', {}).get(modelo_comp, 0)
        depreciacao = parametros.get('