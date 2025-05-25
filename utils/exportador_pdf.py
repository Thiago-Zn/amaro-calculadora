"""exportador_pdf.py - Geração de PDF com dados do voo"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def gerar_pdf(caminho_arquivo, dados: dict):
    c = canvas.Canvas(caminho_arquivo, pagesize=A4)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 800, "Relatório de Custo de Voo - Amaro Aviation")

    c.setFont("Helvetica", 12)
    y = 760
    for chave, valor in dados.items():
        c.drawString(50, y, f"{chave}: R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        y -= 20

    c.showPage()
    c.save()
