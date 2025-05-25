"""exportador_pdf.py - geração de PDF institucional"""
import io
import base64
from datetime import datetime
import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import plotly.io as pio

def create_pdf_report(dados_simulacao, modelo, parametros):
    """
    Gera um relatório em PDF com os resultados da simulação.
    
    Args:
        dados_simulacao (dict): Dados da simulação realizada
        modelo (str): Modelo da aeronave
        parametros (dict): Parâmetros utilizados na simulação
    
    Returns:
        bytes: Conteúdo do PDF em bytes
    """
    
    # Create PDF buffer
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#8c1d40')
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#333333')
    )
    
    section_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.HexColor('#8c1d40')
    )
    
    # Title and header
    story.append(Paragraph("✈️ AMARO AVIATION", title_style))
    story.append(Paragraph("Relatório de Análise de Custos", subtitle_style))
    story.append(Spacer(1, 20))
    
    # Report info
    data_atual = datetime.now().strftime("%d/%m/%Y às %H:%M")
    info_table = Table([
        ['Data do Relatório:', data_atual],
        ['Modelo Analisado:', modelo],
        ['Tipo de Análise:', 'Simulação de Custos Operacionais']
    ], colWidths=[2*inch, 3*inch])
    
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f2f6')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(info_table)
    story.append(Spacer(1, 30))
    
    # Executive Summary
    story.append(Paragraph("RESUMO EXECUTIVO", section_style))
    
    if 'total' in dados_simulacao:
        custo_total = dados_simulacao['total']
        preco_mercado = parametros.get('preco_mercado_hora', {}).get(modelo, 0)
        economia = preco_mercado - custo_total if preco_mercado > custo_total else 0
        
        resumo_text = f"""
        A análise realizada para o modelo {modelo} demonstra os seguintes resultados principais:
        <br/><br/>
        • <b>Custo operacional por hora:</b> R$ {custo_total:,.2f}
        <br/>
        • <b>Preço de mercado por hora:</b> R$ {preco_mercado:,.2f}
        <br/>
        • <b>Economia estimada por hora:</b> R$ {economia:,.2f}
        <br/>
        • <b>Percentual de economia:</b> {(economia/preco_mercado*100):.1f}%
        """
        
        story.append(Paragraph(resumo_text, styles['Normal']))
        story.append(Spacer(1, 20))
    
    # Cost breakdown
    story.append(Paragraph("DETALHAMENTO DE CUSTOS", section_style))
    
    if all(key in dados_simulacao for key in ['preco_comb', 'manut', 'piloto', 'depr']):
        cost_data = [
            ['Componente de Custo', 'Valor (R$)', 'Percentual (%)'],
            ['Combustível', f"{dados_simulacao['preco_comb']:,.2f}", 
             f"{(dados_simulacao['preco_comb']/dados_simulacao['total']*100):.1f}%"],
            ['Manutenção', f"{dados_simulacao['manut']:,.2f}", 
             f"{(dados_simulacao['manut']/dados_simulacao['total']*100):.1f}%"],
            ['Piloto', f"{dados_simulacao['piloto']:,.2f}", 
             f"{(dados_simulacao['piloto']/dados_simulacao['total']*100):.1f}%"],
            ['Depreciação', f"{dados_simulacao['depr']:,.2f}", 
             f"{(dados_simulacao['depr']/dados_simulacao['total']*100):.1f}%"],
            ['TOTAL', f"{dados_simulacao['total']:,.2f}", '100.0%']
        ]
        
        cost_table = Table(cost_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
        cost_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8c1d40')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f0f2f6')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(cost_table)
        story.append(Spacer(1, 20))
    
    # Technical specifications
    story.append(Paragraph("ESPECIFICAÇÕES TÉCNICAS", section_style))
    
    specs_data = [
        ['Parâmetro', 'Valor', 'Unidade'],
        ['Consumo de combustível', f"{parametros.get('consumo_modelos', {}).get(modelo, 0)}", 'L/h'],
        ['Custo de manutenção', f"R$ {parametros.get('custo_manutencao', {}).get(modelo, 0):,.2f}", '/h'],
        ['Custo do piloto', f"R$ {parametros.get('custo_piloto_hora', {}).get(modelo, 0):,.2f}", '/h'],
        ['Depreciação', f"R$ {parametros.get('depreciacao_hora', {}).get(modelo, 0):,.2f}", '/h'],
        ['Preço do combustível', f"R$ {parametros.get('preco_combustivel', 0):.2f}", '/L']
    ]
    
    specs_table = Table(specs_data, colWidths=[2.5*inch, 1.5*inch, 1*inch])
    specs_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8c1d40')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(specs_table)
    story.append(Spacer(1, 30))
    
    # Conclusions
    story.append(Paragraph("CONCLUSÕES E RECOMENDAÇÕES", section_style))
    
    conclusoes = """
    Com base na análise realizada, destacamos:
    <br/><br/>
    1. <b>Viabilidade Econômica:</b> O modelo apresenta economia significativa comparado aos preços de mercado.
    <br/><br/>
    2. <b>Estrutura de Custos:</b> A composição dos custos permite identificar oportunidades de otimização.
    <br/><br/>
    3. <b>Competitividade:</b> Os valores demonstram a competitividade da operação Amaro Aviation.
    <br/><br/>
    4. <b>Planejamento:</b> Os dados fornecem base sólida para planejamento financeiro e operacional.
    """
    
    story.append(Paragraph(conclusoes, styles['Normal']))
    story.append(Spacer(1, 30))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        alignment=TA_CENTER,
        textColor=colors.grey
    )
    
    story.append(Spacer(1, 50))
    story.append(Paragraph("Este relatório foi gerado automaticamente pela Calculadora Amaro Aviation", footer_style))
    story.append(Paragraph(f"Data de geração: {data_atual}", footer_style))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    
    return buffer.getvalue()

def download_pdf_button(pdf_content, filename="relatorio_amaro_aviation.pdf"):
    """
    Cria um botão de download para o PDF gerado.
    
    Args:
        pdf_content (bytes): Conteúdo do PDF
        filename (str): Nome do arquivo para download
    """
    b64 = base64.b64encode(pdf_content).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">📄 Baixar Relatório PDF</a>'
    return href

def generate_streamlit_pdf_download(dados_simulacao, modelo, parametros):
    """
    Função helper para integração com Streamlit.
    Gera o PDF e cria o botão de download.
    
    Args:
        dados_simulacao (dict): Dados da simulação
        modelo (str): Modelo da aeronave
        parametros (dict): Parâmetros utilizados
    """
    try:
        pdf_content = create_pdf_report(dados_simulacao, modelo, parametros)
        filename = f"relatorio_{modelo.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        
        # Create download button
        st.download_button(
            label="📄 Baixar Relatório PDF",
            data=pdf_content,
            file_name=filename,
            mime="application/pdf",
            help="Clique para baixar o relatório detalhado em PDF"
        )
        
        return True
        
    except Exception as e:
        st.error(f"Erro ao gerar PDF: {str(e)}")
        return False

# Example usage function for testing
def exemplo_uso():
    """
    Exemplo de como usar o gerador de PDF.
    """
    dados_exemplo = {
        'total': 5000.0,
        'preco_comb': 2000.0,
        'manut': 1500.0,
        'piloto': 1000.0,
        'depr': 500.0
    }
    
    parametros_exemplo = {
        'consumo_modelos': {'Cessna Citation XLS': 550},
        'custo_manutencao': {'Cessna Citation XLS': 2500},
        'custo_piloto_hora': {'Cessna Citation XLS': 2000},
        'depreciacao_hora': {'Cessna Citation XLS': 15000},
        'preco_combustivel': 8.66,
        'preco_mercado_hora': {'Cessna Citation XLS': 12000}
    }
    
    pdf_bytes = create_pdf_report(dados_exemplo, 'Cessna Citation XLS', parametros_exemplo)
    
    with open('exemplo_relatorio.pdf', 'wb') as f:
        f.write(pdf_bytes)
    
    print("PDF de exemplo gerado com sucesso!")