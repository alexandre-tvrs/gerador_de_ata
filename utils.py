import re
import smtplib
from email import encoders
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from datetime import date, timedelta
from email.mime.multipart import MIMEMultipart


def count_weekdays(start_date, end_date):
    """Conta os dias úteis entre duas datas."""
    day_count = 0
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() < 5:  # 0 = segunda, 4 = sexta
            day_count += 1
        current_date += timedelta(days=1)
    return day_count

def get_sprint_number(today):
    """
    Calcula o número da sprint com base na data atual.
    Cada sprint tem 15 dias úteis (ignora fins de semana).
    A Sprint 0 começa em 07/04/2025.
    """
    sprint_start_date = date(2025, 4, 7)
    
    if today < sprint_start_date:
        return -1  # antes da primeira sprint
    
    # Contar quantos dias úteis se passaram
    total_weekdays = count_weekdays(sprint_start_date, today)
    
    # Cada sprint tem 15 dias úteis
    sprint_number = total_weekdays // 15
    return sprint_number

def adicionar_bloco_codigo(doc, codigo, linguagem=""):
    paragrafo = doc.add_paragraph()
    run = paragrafo.add_run(codigo)
    run.font.name = 'Courier New'
    run.font.size = Pt(10)
    r = run._element
    r.rPr.rFonts.set(qn('w:eastAsia'), 'Courier New')

    # Estilo visual (opcional)
    paragrafo_format = paragrafo.paragraph_format
    paragrafo_format.space_before = Pt(6)
    paragrafo_format.space_after = Pt(6)

    # Borda estilo "caixa de código"
    p = paragrafo._element
    pPr = p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    for side in ['top', 'left', 'bottom', 'right']:
        border = OxmlElement(f'w:{side}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), '4')
        border.set(qn('w:space'), '2')
        border.set(qn('w:color'), 'auto')
        pBdr.append(border)
    pPr.append(pBdr)
    
def substituir_variaveis_em_documento(doc, variaveis):
    # Substitui em parágrafos fora de tabela
    for paragrafo in doc.paragraphs:
        for chave, valor in variaveis.items():
            if f"{{{{{chave}}}}}" in paragrafo.text:
                paragrafo.text = paragrafo.text.replace(f"{{{{{chave}}}}}", valor)

    # Substitui dentro de tabelas
    for tabela in doc.tables:
        for linha in tabela.rows:
            for celula in linha.cells:
                for paragrafo in celula.paragraphs:
                    for chave, valor in variaveis.items():
                        if f"{{{{{chave}}}}}" in paragrafo.text:
                            paragrafo.text = paragrafo.text.replace(f"{{{{{chave}}}}}", valor)

def inserir_resposta_llm(doc, texto):
    # Regex para detectar blocos de código: ```linguagem\n(código)\n```
    padrao = re.compile(r'```(\w+)?\n(.*?)\n```', re.DOTALL)
    pos = 0

    for match in padrao.finditer(texto):
        inicio, fim = match.span()
        linguagem = match.group(1) or ""
        codigo = match.group(2)

        # Texto antes do código
        if inicio > pos:
            trecho = texto[pos:inicio].strip()
            for linha in trecho.splitlines():
                if linha.strip():
                    doc.add_paragraph(linha.strip())
        # Adiciona o bloco de código formatado
        adicionar_bloco_codigo(doc, codigo, linguagem)

        pos = fim

    # Texto depois do último bloco de código
    if pos < len(texto):
        restante = texto[pos:].strip()
        for linha in restante.splitlines():
            if linha.strip():
                doc.add_paragraph(linha.strip())
                
def enviar_email(pdf, dia):
    password = "ojbs qfgx euob kujr"
    sender = "alexandre.tavares@kuaracapital.com"
    # destination = ["manuel@kuaracapital.com", "kaue.figueiredo@kuaracapital.com"]
    destination = "alexandre.j.tavares.jr@gmail.com"
    
    subject = f"[INTERNO] ATA do dia {dia}"
    body = f"""
    Prezados, bom dia.
    
    Segue em anexo a ata das atividades desenvolvidas no dia {dia}.
    
    Fico à disposição para quaisquer esclarecimentos.
    
    Atenciosamente, Alexandre Tavares.
    """
    
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ", ".join(destination) if isinstance(destination, list) else destination
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    with open(pdf, 'rb') as anexo:
        parte = MIMEBase('application', 'octet-stream')
        parte.set_payload(anexo.read())
        encoders.encode_base64(parte)
        parte.add_header('Content-Disposition', f'attachment; filename="{pdf}"')
        msg.attach(parte)
        
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, destination, msg.as_string())
        print("Email enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")