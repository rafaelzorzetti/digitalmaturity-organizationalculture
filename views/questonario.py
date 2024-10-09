import streamlit as st
import pandas as pd
from github import Github
import os
import base64
import io

# Configurar o token de acesso pessoal (PAT) e o repositório
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
REPO_NAME = "rafaelzorzetti/digitalmaturity-organizationalculture"
RESPONSES_CSV_PATH = "data/respostas_questionario.csv"
QUESTIONS_CSV_PATH = "data/questionario_cultura_organizacional.csv"

# Função para carregar o CSV de perguntas do GitHub
def load_questions(file_path):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    file_content = repo.get_contents(file_path)
    csv_content = base64.b64decode(file_content.content).decode('utf-8')
    df = pd.read_csv(io.StringIO(csv_content), sep=';')
    return df

# Função para calcular o índice de maturidade
def calculate_maturity(responses):
    responses = [int(r) for r in responses]  # Garantir que apenas inteiros sejam usados
    total_score = sum(responses)
    average_score = total_score / len(responses)  # Calcular a média dos valores
    maturity_index = round(average_score)  # Arredondar para garantir um valor de 1 a 6
    maturity_index = max(1, min(maturity_index, 6))  # Garantir que o índice fique dentro dos limites de 1 a 6
    return maturity_index

# Função para salvar o CSV de respostas no GitHub
def save_responses_to_github(company_name, responses, maturity_index):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    # Carregar o CSV existente do GitHub
    try:
        file_content = repo.get_contents(RESPONSES_CSV_PATH)
        csv_content = base64.b64decode(file_content.content).decode('utf-8')
        df = pd.read_csv(io.StringIO(csv_content), sep=';')
    except:
        # Se o arquivo não existir, criar um novo DataFrame
        df = pd.DataFrame(columns=['Empresa', 'Respostas', 'Indice_Maturidade'])

    # Preparar os novos dados
    new_data = {'Empresa': company_name, 'Respostas': str(responses), 'Indice_Maturidade': maturity_index}
    new_df = pd.DataFrame([new_data])

    # Adicionar os novos dados ao DataFrame existente
    df = pd.concat([df, new_df], ignore_index=True)

    # Salvar o CSV atualizado
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, sep=';')
    csv_encoded = base64.b64encode(csv_buffer.getvalue().encode()).decode()

    # Verificar se o arquivo já existe no GitHub e atualizar ou criar
    try:
        repo.update_file(file_content.path, "Atualizando respostas", csv_buffer.getvalue(), file_content.sha)
    except:
        repo.create_file(RESPONSES_CSV_PATH, "Adicionando respostas", csv_buffer.getvalue())

# Página do questionário
def page_questionnaire():
    st.title("Avaliação da Maturidade da Cultura Organizacional")
    
    # Campo para o usuário inserir o nome da empresa
    company_name = st.text_input("Digite o nome da empresa:")

    # Carregar o CSV com as perguntas do GitHub
    df = load_questions(QUESTIONS_CSV_PATH)

    # Lista para armazenar as respostas numéricas
    responses = []

    st.header("Por favor, responda às seguintes questões:")

    # Apresentar as perguntas e alternativas
    for index, row in df.iterrows():
        st.subheader(row['Pergunta'].strip())
        response = st.radio(
            f"Selecione sua resposta para a pergunta {index+1}:",
            options=[
                (1, row['Alternativa 1']),
                (2, row['Alternativa 2']),
                (3, row['Alternativa 3']),
                (4, row['Alternativa 4']),
                (5, row['Alternativa 5']),
                (6, row['Alternativa 6'])
            ],
            format_func=lambda x: x[1]
        )
        
        # Armazenar o valor numérico da resposta
        responses.append(response[0])

    # Botão para calcular a maturidade e salvar os dados
    if st.button("Enviar Dados"):
        if company_name:
            maturity_index = calculate_maturity(responses)
            save_responses_to_github(company_name, responses, maturity_index)
            st.success("Dados enviados com sucesso!")
            st.write(f"O índice de maturidade da {company_name} é {maturity_index}")
        else:
            st.error("Por favor, insira o nome da empresa antes de enviar.")

# Chamar a função na página principal
if __name__ == "__main__":
    page_questionnaire()



