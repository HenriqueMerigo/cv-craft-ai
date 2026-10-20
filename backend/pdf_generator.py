import io
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def gerar_pdf(dados_pessoais: dict, dados_ia: dict, idioma: str = "pt") -> bytes:
    buffer = io.BytesIO()
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()

    # Títulos das Seções baseados no idioma
    titulos = {
        "pt": {
            "resumo": "RESUMO PROFISSIONAL",
            "exp": "EXPERIÊNCIA PROFISSIONAL",
            "edu": "FORMAÇÃO ACADÊMICA",
            "hab": "HABILIDADES TÉCNICAS"
        },
        "en": {
            "resumo": "PROFESSIONAL SUMMARY",
            "exp": "WORK EXPERIENCE",
            "edu": "EDUCATION",
            "hab": "TECHNICAL SKILLS"
        }
    }[idioma]

    # Paleta de Cores Premium
    COR_PRIMARIA = colors.HexColor("#0F172A")
    COR_SECUNDARIA = colors.HexColor("#2563EB")
    COR_TEXTO = colors.HexColor("#334155")
    COR_MUTED = colors.HexColor("#64748B")
    COR_LINHA = colors.HexColor("#E2E8F0")

    # Estilos
    estilo_nome = ParagraphStyle("NomeHeader", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=22, leading=26, textColor=COR_PRIMARIA, spaceAfter=3)
    estilo_cargo_topo = ParagraphStyle("CargoTopo", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=COR_SECUNDARIA, spaceAfter=6)
    estilo_contato = ParagraphStyle("ContatoHeader", parent=styles["Normal"], fontName="Helvetica", fontSize=8.5, leading=12, textColor=COR_MUTED, spaceAfter=10)
    estilo_secao = ParagraphStyle("TituloSecao", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=10.5, leading=14, textColor=COR_PRIMARIA, spaceBefore=10, spaceAfter=4)
    estilo_cargo = ParagraphStyle("CargoItem", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=9.5, leading=13, textColor=COR_PRIMARIA)
    estilo_empresa = ParagraphStyle("EmpresaItem", parent=styles["Normal"], fontName="Helvetica-Oblique", fontSize=9, leading=12, textColor=COR_SECUNDARIA)
    estilo_data = ParagraphStyle("DataItem", parent=styles["Normal"], fontName="Helvetica", fontSize=8.5, leading=12, textColor=COR_MUTED, alignment=2)
    estilo_texto = ParagraphStyle("TextoCorpo", parent=styles["Normal"], fontName="Helvetica", fontSize=8.8, leading=12.5, textColor=COR_TEXTO, spaceAfter=2)

    story = []

    # 1. Cabeçalho
    story.append(Paragraph(dados_pessoais.get("nome", "Seu Nome").upper(), estilo_nome))
    if dados_pessoais.get("cargo_desejado"):
        story.append(Paragraph(dados_pessoais.get("cargo_desejado").upper(), estilo_cargo_topo))

    contatos = [dados_pessoais.get("email"), dados_pessoais.get("telefone"), dados_pessoais.get("linkedin")]
    contatos_str = "  •  ".join([c for c in contatos if c])
    story.append(Paragraph(contatos_str, estilo_contato))

    story.append(HRFlowable(width="100%", thickness=1.5, color=COR_SECUNDARIA, spaceBefore=2, spaceAfter=8))

    # 2. Resumo Profissional
    if dados_ia.get("resumo_profissional"):
        story.append(Paragraph(titulos["resumo"], estilo_secao))
        story.append(HRFlowable(width="100%", thickness=0.5, color=COR_LINHA, spaceBefore=2, spaceAfter=6))
        story.append(Paragraph(dados_ia["resumo_profissional"], estilo_texto))
        story.append(Spacer(1, 6))

    # 3. Experiência
    if dados_ia.get("experiencias"):
        story.append(Paragraph(titulos["exp"], estilo_secao))
        story.append(HRFlowable(width="100%", thickness=0.5, color=COR_LINHA, spaceBefore=2, spaceAfter=6))

        for exp in dados_ia["experiencias"]:
            col_esquerda = [
                Paragraph(f"<b>{exp.get('cargo', '')}</b>", estilo_cargo),
                Paragraph(exp.get("empresa", ""), estilo_empresa),
            ]
            col_direita = [Paragraph(exp.get("periodo", ""), estilo_data)]

            tabela_cabecalho = Table([[col_esquerda, col_direita]], colWidths=[380, 143])
            tabela_cabecalho.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
            ]))
            story.append(tabela_cabecalho)

            for bp in exp.get("bullet_points", []):
                story.append(Paragraph(f"• &nbsp; {bp}", estilo_texto))
            story.append(Spacer(1, 6))

    # 4. Formação
    formacao = dados_ia.get("formacao") or dados_pessoais.get("educacao_bruta")
    if formacao:
        story.append(Paragraph(titulos["edu"], estilo_secao))
        story.append(HRFlowable(width="100%", thickness=0.5, color=COR_LINHA, spaceBefore=2, spaceAfter=6))
        story.append(Paragraph(formacao, estilo_texto))
        story.append(Spacer(1, 6))

    # 5. Habilidades
    habilidades = dados_ia.get("habilidades") or dados_pessoais.get("habilidades_lista")
    if habilidades:
        story.append(Paragraph(titulos["hab"], estilo_secao))
        story.append(HRFlowable(width="100%", thickness=0.5, color=COR_LINHA, spaceBefore=2, spaceAfter=6))
        hab_str = "   •   ".join(habilidades) if isinstance(habilidades, list) else habilidades
        story.append(Paragraph(hab_str, estilo_texto))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()