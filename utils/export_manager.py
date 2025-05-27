"""
Gerenciador de exportação unificado para Amaro Aviation Calculator v3.0
Sistema robusto com fallbacks automáticos e interface simplificada
"""

import pandas as pd
import json
import streamlit as st
from datetime import datetime
from pathlib import Path
from io import BytesIO, StringIO
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExportManager:
    """Gerenciador centralizado de exportações"""
    
    def __init__(self):
        self.export_formats = ['excel', 'pdf', 'csv', 'json']
        self.fallback_chain = ['excel', 'csv', 'json']
    
    def create_report_data(self, analysis_type, input_data, results, lang='pt'):
        """
        Cria estrutura padronizada de dados para relatório
        
        Args:
            analysis_type: Tipo da análise
            input_data: Dados de entrada
            results: Resultados calculados
            lang: Idioma do relatório
        
        Returns:
            Dict estruturado para exportação
        """
        return {
            "sistema": "Amaro Aviation Calculator",
            "versao": "3.0",
            "data_geracao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "idioma": lang,
            "tipo_analise": analysis_type,
            "parametros_entrada": input_data,
            "resultados": results,
            "observacoes": "Relatório gerado automaticamente" if lang == 'pt' else "Report generated automatically"
        }
    
    def export_excel(self, report_data, filename=None):
        """
        Exporta para Excel com formatação premium
        
        Args:
            report_data: Dados do relatório
            filename: Nome do arquivo (opcional)
        
        Returns:
            BytesIO buffer ou None se falhar
        """
        try:
            buffer = BytesIO()
            
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                # Criar workbook e worksheet
                workbook = writer.book
                
                # Definir formatos
                header_format = workbook.add_format({
                    'bold': True,
                    'font_color': 'white',
                    'bg_color': '#8c1d40',
                    'align': 'center',
                    'border': 1
                })
                
                currency_format = workbook.add_format({
                    'num_format': 'R$ #,##0.00',
                    'align': 'right'
                })
                
                percentage_format = workbook.add_format({
                    'num_format': '0.0%',
                    'align': 'right'
                })
                
                # Aba 1: Resumo Executivo
                summary_data = []
                summary_data.append(['AMARO AVIATION - RELATÓRIO', ''])
                summary_data.append(['', ''])
                summary_data.append(['Data:', report_data["data_geracao"]])
                summary_data.append(['Análise:', report_data["tipo_analise"]])
                summary_data.append(['Versão:', report_data["versao"]])
                summary_data.append(['', ''])
                
                # Parâmetros
                summary_data.append(['PARÂMETROS', ''])
                for key, value in report_data["parametros_entrada"].items():
                    summary_data.append([key.replace("_", " ").title(), str(value)])
                
                summary_data.append(['', ''])
                
                # Resultados
                summary_data.append(['RESULTADOS', ''])
                for key, value in report_data["resultados"].items():
                    if isinstance(value, (int, float)):
                        if value > 1000:
                            value_str = f"R$ {value:,.2f}"
                        else:
                            value_str = f"{value:.2f}%"
                    else:
                        value_str = str(value)
                    summary_data.append([key.replace("_", " ").title(), value_str])
                
                df_summary = pd.DataFrame(summary_data, columns=["Campo", "Valor"])
                df_summary.to_excel(writer, sheet_name="Resumo Executivo", index=False)
                
                # Formatar primeira aba
                worksheet = writer.sheets["Resumo Executivo"]
                worksheet.set_column('A:A', 25)
                worksheet.set_column('B:B', 20)
                
                # Aba 2: Dados Detalhados
                detailed_data = []
                
                def flatten_dict(d, prefix=""):
                    items = []
                    for k, v in d.items():
                        new_key = f"{prefix}_{k}" if prefix else k
                        if isinstance(v, dict):
                            items.extend(flatten_dict(v, new_key))
                        else:
                            items.append([new_key.replace("_", " ").title(), str(v)])
                    return items
                
                detailed_data = flatten_dict(report_data)
                df_detailed = pd.DataFrame(detailed_data, columns=["Campo", "Valor"])
                df_detailed.to_excel(writer, sheet_name="Dados Completos", index=False)
                
                # Formatar segunda aba
                worksheet2 = writer.sheets["Dados Completos"]
                worksheet2.set_column('A:A', 30)
                worksheet2.set_column('B:B', 25)
            
            buffer.seek(0)
            logger.info(f"Excel exportado com sucesso: {len(buffer.getvalue())} bytes")
            return buffer
            
        except Exception as e:
            logger.error(f"Erro ao exportar Excel: {e}")
            return None
    
    def export_csv(self, report_data, filename=None):
        """
        Exporta para CSV como fallback universal
        
        Args:
            report_data: Dados do relatório
            filename: Nome do arquivo (opcional)
        
        Returns:
            StringIO buffer ou None se falhar
        """
        try:
            csv_data = []
            
            # Cabeçalho
            csv_data.append(["AMARO AVIATION - RELATÓRIO"])
            csv_data.append(["Data", report_data["data_geracao"]])
            csv_data.append(["Análise", report_data["tipo_analise"]])
            csv_data.append(["", ""])
            
            # Parâmetros
            csv_data.append(["PARÂMETROS", ""])
            for k, v in report_data["parametros_entrada"].items():
                csv_data.append([k.replace("_", " ").title(), str(v)])
            
            csv_data.append(["", ""])
            
            # Resultados
            csv_data.append(["RESULTADOS", ""])
            for k, v in report_data["resultados"].items():
                csv_data.append([k.replace("_", " ").title(), str(v)])
            
            df = pd.DataFrame(csv_data, columns=["Campo", "Valor"])
            
            buffer = StringIO()
            df.to_csv(buffer, index=False)
            buffer.seek(0)
            
            logger.info(f"CSV exportado com sucesso")
            return buffer
            
        except Exception as e:
            logger.error(f"Erro ao exportar CSV: {e}")
            return None
    
    def export_json(self, report_data, filename=None):
        """
        Exporta para JSON para backup completo
        
        Args:
            report_data: Dados do relatório
            filename: Nome do arquivo (opcional)
        
        Returns:
            StringIO buffer ou None se falhar
        """
        try:
            buffer = StringIO()
            json.dump(report_data, buffer, indent=2, ensure_ascii=False, default=str)
            buffer.seek(0)
            
            logger.info(f"JSON exportado com sucesso")
            return buffer
            
        except Exception as e:
            logger.error(f"Erro ao exportar JSON: {e}")
            return None
    
    def export_with_fallback(self, report_data, preferred_format='excel', filename_base="amaro_report"):
        """
        Exporta com fallback automático se formato preferido falhar
        
        Args:
            report_data: Dados do relatório
            preferred_format: Formato preferido ('excel', 'csv', 'json')
            filename_base: Base do nome do arquivo
        
        Returns:
            Tuple (buffer, format_used, filename) ou (None, None, None) se tudo falhar
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Tentar formato preferido primeiro
        formats_to_try = [preferred_format] + [f for f in self.fallback_chain if f != preferred_format]
        
        for format_type in formats_to_try:
            try:
                if format_type == 'excel':
                    buffer = self.export_excel(report_data)
                    if buffer:
                        filename = f"{filename_base}_{timestamp}.xlsx"
                        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        return buffer, format_type, filename, mime_type
                
                elif format_type == 'csv':
                    buffer = self.export_csv(report_data)
                    if buffer:
                        filename = f"{filename_base}_{timestamp}.csv"
                        mime_type = "text/csv"
                        return buffer, format_type, filename, mime_type
                
                elif format_type == 'json':
                    buffer = self.export_json(report_data)
                    if buffer:
                        filename = f"{filename_base}_{timestamp}.json"
                        mime_type = "application/json"
                        return buffer, format_type, filename, mime_type
                        
            except Exception as e:
                logger.warning(f"Falha no formato {format_type}: {e}")
                continue
        
        logger.error("Todos os formatos de exportação falharam")
        return None, None, None, None
    
    def create_streamlit_download_button(self, report_data, button_text="📊 Baixar Relatório",
                                       preferred_format='excel', filename_base="amaro_report",
                                       use_container_width=True):
        """
        Cria botão de download no Streamlit com fallback automático
        
        Args:
            report_data: Dados do relatório
            button_text: Texto do botão
            preferred_format: Formato preferido
            filename_base: Base do nome do arquivo
            use_container_width: Usar largura completa do container
        
        Returns:
            True se botão foi criado com sucesso, False caso contrário
        """
        try:
            buffer, format_used, filename, mime_type = self.export_with_fallback(
                report_data, preferred_format, filename_base
            )
            
            if buffer and format_used:
                # Ajustar texto do botão baseado no formato usado
                if format_used != preferred_format:
                    format_names = {
                        'excel': '📊 Excel',
                        'csv': '📋 CSV', 
                        'json': '📄 JSON'
                    }
                    button_text = f"{format_names.get(format_used, format_used.upper())} (Fallback)"
                
                # Criar botão de download
                st.download_button(
                    label=button_text,
                    data=buffer.getvalue(),
                    file_name=filename,
                    mime=mime_type,
                    use_container_width=use_container_width
                )
                
                # Mostrar aviso se usou fallback
                if format_used != preferred_format:
                    st.info(f"ℹ️ Formato {preferred_format.upper()} não disponível. Usando {format_used.upper()} como alternativa.")
                
                return True
            else:
                st.error("❌ Erro: Não foi possível gerar o relatório em nenhum formato disponível.")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao criar botão de download: {e}")
            st.error(f"❌ Erro ao preparar download: {e}")
            return False

# Instância global do gerenciador
export_manager = ExportManager()

# Funções de conveniência para compatibilidade
def criar_relatorio_dados(analysis_type, input_data, results, lang='pt'):
    """Função de conveniência para criar dados de relatório"""
    return export_manager.create_report_data(analysis_type, input_data, results, lang)

def gerar_excel_simples(report_data):
    """Função de conveniência para gerar Excel"""
    return export_manager.export_excel(report_data)

def botao_download_inteligente(report_data, button_text="📊 Baixar Relatório", 
                              preferred_format='excel', filename_base="amaro_report"):
    """Função de conveniência para criar botão com fallback"""
    return export_manager.create_streamlit_download_button(
        report_data, button_text, preferred_format, filename_base
    )

# Exemplo de uso
if __name__ == "__main__":
    # Dados de teste
    test_input = {
        "modelo": "Pilatus PC-12",
        "horas_mes": 80,
        "ocupacao": 75
    }
    
    test_results = {
        "receita_bruta": 480000,
        "custo_operacional": 320000,
        "lucro_liquido": 144000,
        "roi_mensal": 45.0
    }
    
    # Teste do sistema
    manager = ExportManager()
    report_data = manager.create_report_data("Teste", test_input, test_results)
    
    # Testar exportações
    excel_buffer = manager.export_excel(report_data)
    csv_buffer = manager.export_csv(report_data)
    json_buffer = manager.export_json(report_data)
    
    print("=== Teste Export Manager ===")
    print(f"Excel: {'✅' if excel_buffer else '❌'}")
    print(f"CSV: {'✅' if csv_buffer else '❌'}")
    print(f"JSON: {'✅' if json_buffer else '❌'}")
    
    # Teste com fallback
    buffer, format_used, filename, mime = manager.export_with_fallback(report_data)
    print(f"Fallback: {'✅' if buffer else '❌'} (formato: {format_used})")
    print("✅ Testes concluídos!")