import requests

def ia(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "ata-mistral",
            "prompt": prompt,
            "stream": False,
    })
    
    return response.json()["response"]

def analyze_markdown_content(activity_file_content):
    prompt = f"""
    Você é um assistente encarregado de analisar um arquivo Markdown com anotações de atividades realizadas no dia.

    Seu objetivo é **organizar e estruturar o conteúdo**, mantendo a hierarquia de tópicos e subtópicos, e identificando os seguintes elementos:

    - Blocos de código (dentro de três crases ```), não crie novos códigos, apenas organize os existentes.
    - Referências a imagens (no formato `![descrição](caminho)`)
    - Descrições técnicas ou textuais
    - Tópicos e subtópicos com indentação clara

    ⚠️ **Não formate como ATA ainda. Não use linguagem formal ainda. Apenas organize.**

    Apresente a estrutura organizada do seguinte conteúdo Markdown:

    {activity_file_content}
    """
    
    return ia(prompt)

def generate_formal_ata_from_analysis(organized_content, ata_date):
    prompt = f"""
    Você é um assistente encarregado de gerar uma **ATA de atividades formal e clara**, com base no conteúdo organizado a seguir.

    Siga estas diretrizes com rigor:

    ---

    ### 🎯 Objetivo
    Redigir a ATA em português formal, mantendo toda a estrutura e informações técnicas presentes.

    ---

    ### 🧭 Instruções de formatação:

    1. **Idioma**: Use sempre português formal e claro.
    2. **Estrutura**: Mantenha a hierarquia de tópicos e subtópicos.
    3. **Código**: Preserve blocos de código com ``` e indentação correta, não altere o conteúdo. Também não crie códigos que não estão no conteúdo original.
    4. **Imagens**: Mantenha no formato `![descrição](caminho)`
    5. **Evite repetições**, rodeios ou informalidades.

    ---

    ### ✅ Exemplo de início esperado:

    Durante o dia {ata_date}, foram realizadas as seguintes atividades:
    - Reunião com a equipe de desenvolvimento
        - Discussão sobre progresso da sprint atual e próximos passos.
        - Implementação de novas funcionalidades no sistema de gestão de tarefas.
        - Revisão do código existente para melhorias de desempenho.
        
    - Teste de integração do sistema de pagamentos
        - Implementação de testes automatizados para garantir a qualidade do código.
        - Revisão e atualização da documentação técnica.
        
    Segue abaixo uma melhor descrição das atividades realizadas:

    #### Reunião com a equipe de desenvolvimento

    Discussão sobre progresso da sprint atual e próximos passos.

    ##### Implementações

    - Implementação de novas funcionalidades no sistema de gestão de tarefas.
    - Revisão do código existente para melhorias de desempenho.
    
    
    Gere agora a ATA com base no conteúdo abaixo:

    {organized_content}
    """
    return ia(prompt)

def generate_ata(content, ata_date):
    organized_content = analyze_markdown_content(content)
    formal_ata = generate_formal_ata_from_analysis(organized_content, ata_date)
    return formal_ata