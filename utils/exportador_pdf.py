"""exportador_pdf.py - Sistema de exportação PDF premium com identidade visual Amaro"""

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from pathlib import Path
from datetime import datetime
import io

# Cores Amaro Aviation
AMARO_PRIMARY = HexColor('#8c1d40')
AMARO_SECONDARY = HexColor('#a02050')
AMARO_DARK = HexColor('#2C3E50')
AMARO_LIGHT = HexColor('#F8F9FA')

def criar_estilos():
    """Cria estilos personalizados para o PDF"""
    styles = getSampleStyleSheet()
    
    # Título principal
    styles.add(ParagraphStyle(
        name='TituloAmaro',
        parent=styles['Title'],
        fontSize=24,
        textColor=AMARO_PRIMARY,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))
    
    # Subtítulo
    styles.add(ParagraphStyle(
        name='SubtituloAmaro',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=AMARO_DARK,
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    ))
    
    # Texto destacado
    styles.add(ParagraphStyle(
        name='DestaqueAmaro',
        parent=styles['Normal'],
        fontSize=12,
        textColor=AMARO_PRIMARY,
        fontName='Helvetica-Bold',
        spaceAfter=6
    ))
    
    # Texto normal
    styles.add(ParagraphStyle(
        name='NormalAmaro',
        parent=styles['Normal'],
        fontSize=11,
        textColor=AMARO_DARK,
        spaceAfter=6,
        fontName='Helvetica'
    ))
    
    # Footer
    styles.add(ParagraphStyle(
        name='FooterAmaro',
        parent=styles['Normal'],
        fontSize=9,
        textColor=AMARO_DARK,
        alignment=TA_CENTER,
        fontName='Helvetica'
    ))
    
    return styles

def criar_cabecalho():
    """Cria o cabeçalho premium do documento"""
    elementos = []
    
    # Verificar se existe logo
    logo_path = Path("assets/logo_amaro.png")
    if logo_path.exists():
        try:
            logo = Image(str(logo_path), width=60*mm, height=20*mm)
            elementos.append(logo)
            elementos.append(Spacer(1, 10*mm))
        except:
            # Se não conseguir carregar a logo, usar texto
            pass
    
    # Título da empresa
    styles = criar_estilos()
    titulo_empresa = Paragraph("✈️ AMARO AVIATION", styles['TituloAmaro'])
    elementos.append(titulo_empresa)
    
    subtitulo = Paragraph("RELATÓRIO DE ANÁLISE DE CUSTOS", styles['SubtituloAmaro'])
    elementos.append(subtitulo)
    
    # Linha decorativa
    linha = HRFlowable(width="100%", thickness=2, color=AMARO_PRIMARY)
    elementos.append(linha)
    elementos.append(Spacer(1, 10*mm))
    
    return elementos

def criar_secao_informacoes(dados):
    """Cria seção com informações gerais do relatório"""
    elementos = []
    styles = criar_estilos()
    
    elementos.append(Paragraph("INFORMAÇÕES GERAIS", styles['SubtituloAmaro']))
    
    # Dados da análise
    info_data = [
        ['Data do Relatório:', datetime.now().strftime('%d/%m/%Y %H:%M')],
        ['Tipo de Análise:', dados.get('Análise', 'Não especificado')],
        ['Modelo da Aeronave:', dados.get('Modelo', 'Não especificado')],
        ['Rota:', dados.get('Rota', 'Não especificado')],
        ['Duração:', dados.get('Duração', 'Não especificado')]
    ]
    
    tabela_info = Table(info_data, colWidths=[45*mm, 80*mm])
    tabela_info.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TEXTCOLOR', (0, 0), (0, -1), AMARO_PRIMARY),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    elementos.append(tabela_info)
    elementos.append(Spacer(1, 8*mm))
    
    return elementos

def criar_secao_custos(dados):
    """Cria seção detalhada de custos"""
    elementos = []
    styles = criar_estilos()
    
    elementos.append(Paragraph("BREAKDOWN DE CUSTOS", styles['SubtituloAmaro']))
    
    # Dados dos custos
    custos_data = [
        ['COMPONENTE', 'VALOR (R$)', 'DESCRIÇÃO'],
    ]
    
    # Adicionar componentes de custo
    componentes = [
        ('Combustível', 'Combustível'),
        ('Piloto', 'Piloto'),
        ('Manutenção', 'Manutenção'),
        ('Depreciação', 'Depreciação')
    ]
    
    for nome, chave in componentes:
        if chave in dados:
            valor = dados[chave]
            if isinstance(valor, (int, float)):
                custos_data.append([
                    nome,
                    f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                    f"Custo de {nome.lower()} para este voo"
                ])
    
    # Linha de total
    if 'Custo Total Amaro' in dados:
        custos_data.append(['', '', ''])  # Linha vazia
        custos_data.append([
            'TOTAL AMARO AVIATION',
            f"R$ {dados['Custo Total Amaro']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            'Custo total da operação'
        ])
    
    tabela_custos = Table(custos_data, colWidths=[50*mm, 35*mm, 70*mm])
    tabela_custos.setStyle(TableStyle([
        # Cabeçalho
        ('BACKGROUND', (0, 0), (-1, 0), AMARO_PRIMARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        
        # Dados
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),  # Valores alinhados à direita
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        
        # Total
        ('BACKGROUND', (0, -1), (-1, -1), AMARO_LIGHT),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, -1), (0, -1), AMARO_PRIMARY),
        
        # Bordas
        ('GRID', (0, 0), (-1, -1), 1, AMARO_DARK),
        ('LINEBELOW', (0, 0), (-1, 0), 2, AMARO_PRIMARY),
        
        # Padding
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    elementos.append(tabela_custos)
    elementos.append(Spacer(1, 8*mm))
    
    return elementos

def criar_secao_comparativo(dados):
    """Cria seção de comparativo com mercado"""
    elementos = []
    styles = criar_estilos()
    
    elementos.append(Paragraph("COMPARATIVO COM MERCADO", styles['SubtituloAmaro']))
    
    # Dados do comparativo
    comparativo_data = [
        ['MÉTRICA', 'AMARO AVIATION', 'MERCADO', 'DIFERENÇA'],
    ]
    
    custo_amaro = dados.get('Custo Total Amaro', 0)
    preco_mercado = dados.get('Preço Mercado', 0)
    economia = dados.get('Economia', 0)
    
    comparativo_data.append([
        'Custo Total',
        f"R$ {custo_amaro:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        f"R$ {preco_mercado:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        f"R$ {economia:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    ])
    
    # Percentual de economia
    if preco_mercado > 0:
        percentual = (economia / preco_mercado) * 100
        comparativo_data.append([
            'Percentual de Economia',
            '-',
            '-',
            f"{percentual:.1f}%"
        ])
    
    tabela_comparativo = Table(comparativo_data, colWidths=[45*mm, 35*mm, 35*mm, 35*mm])
    tabela_comparativo.setStyle(TableStyle([
        # Cabeçalho
        ('BACKGROUND', (0, 0), (-1, 0), AMARO_SECONDARY),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        
        # Dados
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        
        # Destaque da economia
        ('TEXTCOLOR', (3, 1), (3, -1), AMARO_PRIMARY),
        ('FONTNAME', (3, 1), (3, -1), 'Helvetica-Bold'),
        
        # Bordas e padding
        ('GRID', (0, 0), (-1, -1), 1, AMARO_DARK),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    elementos.append(tabela_comparativo)
    elementos.append(Spacer(1, 8*mm))
    
    return elementos

def criar_secao_conclusoes(dados):
    """Cria seção de conclusões e insights"""
    elementos = []
    styles = criar_estilos()
    
    elementos.append(Paragraph("CONCLUSÕES E INSIGHTS", styles['SubtituloAmaro']))
    
    economia = dados.get('Economia', 0)
    
    if economia > 0:
        texto_conclusao = f"""
        <b>✅ RESULTADO POSITIVO:</b> A operação com Amaro Aviation apresenta economia significativa 
        de R$ {economia:,.2f} em relação ao preço de mercado para esta rota.
        <br/><br/>
        <b>💡 RECOMENDAÇÕES:</b>
        <br/>• Esta rota demonstra excelente viabilidade econômica
        <br/>• Considere aumentar a frequência nesta rota
        <br/>• Utilize estes dados em apresentações comerciais
        """
    else:
        texto_conclusao = f"""
        <b>⚠️ ATENÇÃO:</b> O custo da operação está R$ {abs(economia):,.2f} acima do preço de mercado.
        <br/><br/>
        <b>🔧 RECOMENDAÇÕES:</b>
        <br/>• Revisar parâmetros operacionais
        <br/>• Analisar eficiência de combustível
        <br/>• Considerar otimização de rotas
        """
    
    conclusao = Paragraph(texto_conclusao.replace(",", "X").replace(".", ",").replace("X", "."), 
                         styles['NormalAmaro'])
    elementos.append(conclusao)
    elementos.append(Spacer(1, 10*mm))
    
    return elementos

def criar_rodape():
    """Cria rodapé do documento"""
    elementos = []
    styles = criar_estilos()
    
    # Linha decorativa
    linha = HRFlowable(width="100%", thickness=1, color=AMARO_PRIMARY)
    elementos.append(linha)
    elementos.append(Spacer(1, 3*mm))
    
    # Texto do rodapé
    rodape_texto = """
    Este relatório foi gerado automaticamente pela Calculadora Amaro Aviation.<br/>
    Para mais informações, entre em contato com nossa equipe técnica.<br/>
    <b>Amaro Aviation</b> - Excelência em Aviação Executiva
    """
    
    rodape = Paragraph(rodape_texto, styles['FooterAmaro'])
    elementos.append(rodape)
    
    return elementos

def gerar_pdf(buffer_arquivo, dados: dict):
    """
    Gera PDF premium com identidade visual Amaro Aviation
    
    Args:
        buffer_arquivo: Buffer para salvar o PDF (BytesIO ou caminho do arquivo)
        dados: Dicionário com os dados para o relatório
    """
    try:
        # Configurar documento
        if isinstance(buffer_arquivo, (str, Path)):
            doc = SimpleDocTemplate(
                str(buffer_arquivo),
                pagesize=A4,
                rightMargin=20*mm,
                leftMargin=20*mm,
                topMargin=25*mm,
                bottomMargin=25*mm
            )
        else:
            doc = SimpleDocTemplate(
                buffer_arquivo,
                pagesize=A4,
                rightMargin=20*mm,
                leftMargin=20*mm,
                topMargin=25*mm,
                bottomMargin=25*mm
            )
        
        # Construir elementos do PDF
        elementos = []
        
        # Cabeçalho
        elementos.extend(criar_cabecalho())
        
        # Informações gerais
        elementos.extend(criar_secao_informacoes(dados))
        
        # Breakdown de custos
        elementos.extend(criar_secao_custos(dados))
        
        # Comparativo
        elementos.extend(criar_secao_comparativo(dados))
        
        # Conclusões
        elementos.extend(criar_secao_conclusoes(dados))
        
        # Rodapé
        elementos.extend(criar_rodape())
        
        # Gerar PDF
        doc.build(elementos)
        
        return True
        
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        return False