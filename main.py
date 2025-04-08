import os
from datetime import date
from docx import Document
from ata import generate_ata
from docx2pdf import convert
from modal import abrir_date_picker
from utils import get_sprint_number, inserir_resposta_llm, substituir_variaveis_em_documento, enviar_email

obsidian_path = r"C:\Users\Alexandre\Documents\Obsidian Vault\Kuará Capital\Sprints"

def main():
    print(f"Gerar ATA de hoje? ({date.today()})")
    res = input("S/N: ")
    if res.strip().lower() == 's':
        date_ata = date.today()
        
    elif res.strip().lower() != 's':
        date_ata = abrir_date_picker()
        date_ata = date.fromisoformat(date_ata)
        
    print(date_ata)
        
    sprint = get_sprint_number(date_ata)
    activity_file = os.path.join(obsidian_path, str(sprint), f"{date_ata.strftime('%d-%m-%Y')}.md")
        
    print("Confirme as informações abaixo:")
    print(f"1. Data: {date_ata}")
    print(f"2. Sprint: Sprint {sprint}")
    print(f"3. Arquivo de atividade: {activity_file}")
    input("Pressione Enter para continuar ou Ctrl+C para cancelar.")
    
    with open(activity_file, "r", encoding="utf-8") as file:
        content = file.read()

    # 2. Envia para a LLM e recebe o texto da ATA
    text = generate_ata(content, date_ata)

    # 3. Abre o template Word
    template_file = "ATA.docx"
    doc = Document(template_file)

    variaveis = {
        "nome_colaborador": "Alexandre Tavares",
        "data_ata": date_ata.strftime("%d/%m/%Y"),
        "sprint": str(sprint),
    }

    substituir_variaveis_em_documento(doc, variaveis)

    # 5. Encontra o marcador {{texto}}, remove, e insere o conteúdo da LLM formatado
    for par in doc.paragraphs:
        if "{{texto}}" in par.text:
            par.clear()
            inserir_resposta_llm(doc, text)
            break

    # 6. Salva o arquivo final
    output_docx = f"ATA_{date_ata.strftime('%d-%m-%Y')}.docx"
    doc.save(output_docx)

    # 7. Converte para PDF (você já usa `convert`)
    convert(output_docx, output_docx.replace(".docx", ".pdf"))
    os.remove(output_docx)
    
    enviar_email(output_docx.replace(".docx", ".pdf"), date_ata.strftime("%d/%m/%Y"))
    
if __name__ == "__main__":
    main()