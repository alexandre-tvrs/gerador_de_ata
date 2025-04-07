import os
from datetime import date
from utils import get_sprint_number, preencher_template
from ata import generate_ata

obsidian_path = r"C:\Users\Alexandre\Documents\Obsidian Vault\Kuará Capital\Sprints"

def main():
    print(f"Gerar ATA de hoje? ({date.today()})")
    print("Confirme as informações abaixo:")
    print(f"1. Data: {date.today()}")
    print(f"2. Sprint: Sprint {get_sprint_number(date.today())}")
    
    activity_file = os.path.join(obsidian_path, str(get_sprint_number(date.today())), f"{date.today().strftime("%d-%m-%Y")}.md")
    print(f"3. Arquivo de atividade: {activity_file}")
    
    input("Pressione Enter para continuar ou Ctrl+C para cancelar.")
    
    with open(activity_file, "r", encoding="utf-8") as file:
        content = file.read()
    
    text = generate_ata(content)
    
    template_file = "ATA.docx"
    
    variaveis = {
        "nome_colaborador": "Alexandre Tavares",
        "data_ata": str(date.today().strftime("%d/%m/%Y")),
        "sprint": str(get_sprint_number(date.today())),
        "texto": text,
    }
    
    preencher_template(template_file, f"ATA_{date.today().strftime('%d-%m-%Y')}.docx", variaveis)
    
if __name__ == "__main__":
    main()