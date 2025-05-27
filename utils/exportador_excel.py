"""
Sistema de exportação simplificado e robusto para Amaro Aviation
Focado em funcionalidade e experiência do usuário
"""

import pandas as pd
import json
from datetime import datetime
from pathlib import Path
import io

def criar_relatorio_dados(tipo_analise, dados_entrada, resultados):
    """
    Cria estrutura de dados padronizada para relatórios
    
    Args:
        tipo_analise: Tipo da análise (ex: "Lucro Mensal", "Comparativo")
        dados_entrada: Dicionário com parâmetros de entrada
        resultados: Dicionário com resultados calculados
    
    Returns:
        Dict com dados estruturados para exportação
    """
    relatorio = {
        # Cabeçalho
        "sistema": "Amaro Aviation Calculator",
        "versao": "3.0",
        "data_geracao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "tipo_analise": tipo_analise,
        
        # Dados de entrada
        "parametros_entrada": dados_entrada,
        
        # Resultados
        "resultados": resultados,
        
        # Metadados
        "observacoes": "Relatório gerado automaticamente pelo sistema Amaro Aviation"
    }
    
    return relatorio

def gerar_excel_simples(dados_relatorio):
    """
    Gera arquivo Excel simples usando apenas pandas
    Funciona mesmo sem openpyxl instalado
    
    Args:
        dados_relatorio: Dicionário com dados do relatório
    
    Returns:
        BytesIO buffer com arquivo Excel
    """
    try:
        buffer = io.BytesIO()
        
        # Criar abas separadas
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            
            # Aba 1: Resumo Executivo
            resumo_data = []
            resumo_data.append(["AMARO AVIATION - RELATÓRIO DE ANÁLISE", ""])
            resumo_data.append(["", ""])
            resumo_data.append(["Data:", dados_relatorio["data_geracao"]])
            resumo_data.append(["Tipo de Análise:", dados_relatorio["tipo_analise"]])
            resumo_data.append(["Versão do Sistema:", dados_relatorio["versao"]])
            resumo_data.append(["", ""])
            
            # Adicionar parâmetros de entrada
            resumo_data.append(["PARÂMETROS DE ENTRADA", ""])
            for chave, valor in dados_relatorio["parametros_entrada"].items():
                resumo_data.append([chave.replace("_", " ").title(), str(valor)])
            
            resumo_data.append(["", ""])
            
            # Adicionar resultados
            resumo_data.append(["RESULTADOS", ""])
            for chave, valor in dados_relatorio["resultados"].items():
                if isinstance(valor, (int, float)):
                    if valor > 1000:
                        valor_str = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                    else:
                        valor_str = f"{valor:.2f}%"
                else:
                    valor_str = str(valor)
                resumo_data.append([chave.replace("_", " ").title(), valor_str])
            
            df_resumo = pd.DataFrame(resumo_data, columns=["Campo", "Valor"])
            df_resumo.to_excel(writer, sheet_name="Resumo Executivo", index=False)
            
            # Aba 2: Dados Brutos
            dados_brutos = []
            
            # Achatar todos os dados para tabela
            def achatar_dict(d, prefixo=""):
                items = []
                for k, v in d.items():
                    novo_key = f"{prefixo}_{k}" if prefixo else k
                    if isinstance(v, dict):
                        items.extend(achatar_dict(v, novo_key))
                    else:
                        items.append([novo_key, str(v)])
                return items
            
            dados_brutos = achatar_dict(dados_relatorio)
            df_brutos = pd.DataFrame(dados_brutos, columns=["Campo", "Valor"])
            df_brutos.to_excel(writer, sheet_name="Dados Completos", index=False)
        
        buffer.seek(0)
        return buffer
        
    except Exception as e:
        print(f"Erro ao gerar Excel: {e}")
        return None

def gerar_csv_simples(dados_relatorio):
    """
    Gera arquivo CSV como fallback universal
    
    Args:
        dados_relatorio: Dicionário com dados do relatório
    
    Returns:
        StringIO buffer com arquivo CSV
    """
    try:
        # Criar lista de dados tabulares
        csv_data = []
        
        # Cabeçalho
        csv_data.append(["AMARO AVIATION - RELATÓRIO"])
        csv_data.append(["Data", dados_relatorio["data_geracao"]])
        csv_data.append(["Tipo", dados_relatorio["tipo_analise"]])
        csv_data.append(["", ""])
        
        # Parâmetros
        csv_data.append(["PARÂMETROS", ""])
        for k, v in dados_relatorio["parametros_entrada"].items():
            csv_data.append([k, str(v)])
        
        csv_data.append(["", ""])
        
        # Resultados
        csv_data.append(["RESULTADOS", ""])
        for k, v in dados_relatorio["resultados"].items():
            csv_data.append([k, str(v)])
        
        # Converter para DataFrame e CSV
        df = pd.DataFrame(csv_data, columns=["Campo", "Valor"])
        
        buffer = io.StringIO()
        df.to_csv(buffer, index=False)
        buffer.seek(0)
        
        return buffer
        
    except Exception as e:
        print(f"Erro ao gerar CSV: {e}")
        return None

def gerar_relatorio_pdf_texto(dados_relatorio):
    """
    Gera relatório em formato texto para PDF simples
    
    Args:
        dados_relatorio: Dicionário com dados do relatório
        
    Returns:
        String formatada para PDF ou impressão
    """
    try:
        texto = []
        
        # Cabeçalho
        texto.append("="*60)
        texto.append("✈️  AMARO AVIATION - RELATÓRIO DE ANÁLISE")
        texto.append("="*60)
        texto.append("")
        texto.append(f"Data: {dados_relatorio['data_geracao']}")
        texto.append(f"Tipo de Análise: {dados_relatorio['tipo_analise']}")
        texto.append(f"Sistema: {dados_relatorio['sistema']} v{dados_relatorio['versao']}")
        texto.append("")
        
        # Parâmetros de entrada
        texto.append("-"*40)
        texto.append("PARÂMETROS DE ENTRADA")
        texto.append("-"*40)
        
        for chave, valor in dados_relatorio["parametros_entrada"].items():
            nome_campo = chave.replace("_", " ").title()
            texto.append(f"{nome_campo}: {valor}")
        
        texto.append("")
        
        # Resultados
        texto.append("-"*40)
        texto.append("RESULTADOS DA ANÁLISE")
        texto.append("-"*40)
        
        for chave, valor in dados_relatorio["resultados"].items():
            nome_campo = chave.replace("_", " ").title()
            if isinstance(valor, (int, float)):
                if valor > 1000:
                    valor_fmt = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                else:
                    valor_fmt = f"{valor:.2f}%"
            else:
                valor_fmt = str(valor)
            texto.append(f"{nome_campo}: {valor_fmt}")
        
        texto.append("")
        
        # Observações
        texto.append("-"*40)
        texto.append("OBSERVAÇÕES")
        texto.append("-"*40)
        texto.append(dados_relatorio["observacoes"])
        texto.append("")
        texto.append("Este relatório foi gerado automaticamente.")
        texto.append("Para mais informações, contate a equipe Amaro Aviation.")
        texto.append("")
        texto.append("="*60)
        
        return "\n".join(texto)
        
    except Exception as e:
        print(f"Erro ao gerar relatório texto: {e}")
        return None

def exportar_json_backup(dados_relatorio):
    """
    Exporta dados em JSON para backup completo
    
    Args:
        dados_relatorio: Dicionário com dados do relatório
        
    Returns:
        StringIO buffer com JSON
    """
    try:
        buffer = io.StringIO()
        json.dump(dados_relatorio, buffer, indent=2, ensure_ascii=False, default=str)
        buffer.seek(0)
        return buffer
        
    except Exception as e:
        print(f"Erro ao gerar JSON: {e}")
        return None

# Funções utilitárias para Streamlit
def botao_download_excel(dados_relatorio, nome_arquivo="relatorio_amaro"):
    """
    Cria botão de download Excel no Streamlit
    
    Args:
        dados_relatorio: Dados do relatório
        nome_arquivo: Nome base do arquivo
        
    Returns:
        True se botão foi criado com sucesso
    """
    try:
        import streamlit as st
        
        buffer_excel = gerar_excel_simples(dados_relatorio)
        
        if buffer_excel:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.download_button(
                label="📊 Baixar Relatório Excel",
                data=buffer_excel.getvalue(),
                file_name=f"{nome_arquivo}_{timestamp}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            return True
        else:
            # Fallback para CSV
            buffer_csv = gerar_csv_simples(dados_relatorio)
            if buffer_csv:
                st.download_button(
                    label="📋 Baixar Relatório CSV",
                    data=buffer_csv.getvalue(),
                    file_name=f"{nome_arquivo}_{timestamp}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                return True
            
        return False
        
    except Exception as e:
        print(f"Erro ao criar botão download: {e}")
        return False

def botao_download_relatorio_texto(dados_relatorio, nome_arquivo="relatorio_amaro"):
    """
    Cria botão de download de relatório em texto
    
    Args:
        dados_relatorio: Dados do relatório
        nome_arquivo: Nome base do arquivo
        
    Returns:
        True se botão foi criado com sucesso
    """
    try:
        import streamlit as st
        
        texto_relatorio = gerar_relatorio_pdf_texto(dados_relatorio)
        
        if texto_relatorio:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.download_button(
                label="📄 Baixar Relatório Texto",
                data=texto_relatorio,
                file_name=f"{nome_arquivo}_{timestamp}.txt",
                mime="text/plain",
                use_container_width=True
            )
            return True
            
        return False
        
    except Exception as e:
        print(f"Erro ao criar botão download texto: {e}")
        return False

# Exemplo de uso
if __name__ == "__main__":
    # Dados de exemplo
    dados_teste = {
        "modelo": "Pilatus PC-12",
        "horas_mes": 80,
        "ocupacao": 75
    }
    
    resultados_teste = {
        "receita_bruta": 480000,
        "custo_operacional": 320000,
        "lucro_liquido": 144000,
        "roi_mensal": 45.0
    }
    
    relatorio = criar_relatorio_dados("Lucro Mensal", dados_teste, resultados_teste)
    
    # Testar exportações
    excel_buffer = gerar_excel_simples(relatorio)
    csv_buffer = gerar_csv_simples(relatorio)
    texto_relatorio = gerar_relatorio_pdf_texto(relatorio)
    json_buffer = exportar_json_backup(relatorio)
    
    print("✅ Testes de exportação concluídos")
    print(f"Excel: {'✅' if excel_buffer else '❌'}")
    print(f"CSV: {'✅' if csv_buffer else '❌'}")
    print(f"Texto: {'✅' if texto_relatorio else '❌'}")
    print(f"JSON: {'✅' if json_buffer else '❌'}")