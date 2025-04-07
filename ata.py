import os
import requests

def ia(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False,
    })
    
    return response.json()["response"]

def generate_ata(activity_file):
    prompt = f"""
    Você é um assistente de IA que ajuda a gerar o texto para atas de atividades os dias de sprints, ou seja, não é necessário incluir informações como o nome do cliente, o nome do projeto, etc, apenas pegue as informações das atividades desenvolvidas e gere uma ata.
    Você deve gerar uma ata com as informações enviadas. Também lembre-se de incluir o link para as imagens encontradas no arquivo markdown. Lembre-se que estamos falando de ATAs de atividades, não de reuniões.
    O arquivo markdown é o seguinte:
    {activity_file}
    Caso tenha partes de código, você deve colocar entre três crases (```), e caso tenha imagens, você deve colocar o link da imagem entre colchetes e parênteses, como por exemplo: ![imagem](link_da_imagem).
    Você deve gerar um texto em português, com uma formatação adequada para uma ata de atividades. Não inclua informações que não sejam relevantes para a ata.
    """
    
    return ia(prompt)