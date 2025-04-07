import os
from docx import Document
from docx2pdf import convert
from datetime import date, timedelta

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

def preencher_template(caminho_template, caminho_saida, variaveis):
    doc = Document(caminho_template)

    # Substitui variáveis em parágrafos normais
    for paragrafo in doc.paragraphs:
        for chave, valor in variaveis.items():
            if f"{{{{{chave}}}}}" in paragrafo.text:
                paragrafo.text = paragrafo.text.replace(f"{{{{{chave}}}}}", valor)

    # Substitui variáveis dentro de tabelas
    for tabela in doc.tables:
        for linha in tabela.rows:
            for celula in linha.cells:
                for paragrafo in celula.paragraphs:
                    for chave, valor in variaveis.items():
                        if f"{{{{{chave}}}}}" in paragrafo.text:
                            paragrafo.text = paragrafo.text.replace(f"{{{{{chave}}}}}", valor)

    doc.save(caminho_saida)
    
    convert(caminho_saida, caminho_saida.replace(".docx", ".pdf"))
    
    os.remove(caminho_saida)