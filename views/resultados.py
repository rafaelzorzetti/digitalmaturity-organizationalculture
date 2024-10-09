import streamlit as st
import pandas as pd
import openai
import os
import base64
from github import Github
import io

# Acessando a chave armazenada nos secrets do Streamlit
openai.api_key = st.secrets["OPENAI_API_KEY"]
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
REPO_NAME = "rafaelzorzetti/digitalmaturity-organizationalculture"
RESPONSES_CSV_PATH = "data/respostas_questionario.csv"

# Função para carregar o CSV do GitHub
def load_responses_csv():
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    file_content = repo.get_contents(RESPONSES_CSV_PATH)
    csv_content = base64.b64decode(file_content.content).decode('utf-8')
    df = pd.read_csv(io.StringIO(csv_content), sep=';')
    return df

# Função para exibir as barras lado a lado, coladas
def display_bars(maturity_index):
    colors_active = ["#48BFE3", "#4EA8DE", "#5390CD", "#5E60CE", "#6930C3", "#7400B8"]
    colors_inactive = ["#48BFE333", "#4EA8DE33", "#5390CD33", "#5E60CE33", "#6930C333", "#7400B833"]
    levels = ["Resistência Inicial", "Adaptação Incipiente", "Colaboração Emergente", 
              "Experim. Aprendizado", "Transparência Autonomia", "Inovação Orgânica"]

    cols = st.columns(6)
    for i, col in enumerate(cols):
        bar_color = colors_active[i] if i == (maturity_index - 1) else colors_inactive[i]
        text_style = "font-weight:bold; color:black;" if i == (maturity_index - 1) else "opacity:0.5;"
        with col:
            st.markdown(f"<div style='background-color:{bar_color}; height:30px;'></div>", unsafe_allow_html=True)
            st.markdown(f"<p style='{text_style}; white-space: normal; text-align: center; min-height: 60px; line-height: 1.5; overflow-wrap: break-word;'>{levels[i]}</p>", unsafe_allow_html=True)

# Perguntas a serem usadas no prompt
perguntas = [
    "Disposição para Mudança: Como a organização e os colaboradores lidam com a necessidade de mudanças?",
    "Incentivo à Experimentação: Qual é a atitude da organização em relação à experimentação e aos erros?",
    "Abertura às Novas Ideias: Como a organização recebe e implementa novas ideias propostas pelos colaboradores?",
    "Espírito Colaborativo: Qual é o nível de colaboração entre os colaboradores e equipes?",
    "Liderança Democrática: Como a liderança envolve os colaboradores nas decisões e valoriza suas contribuições?",
    "Comunicação Aberta: Como a organização promove a comunicação entre colaboradores e departamentos?",
    "Transparência: Como a organização pratica a transparência em seus processos e informações?",
    "Capacidade de Antecipação e Adaptação: Como a organização se prepara e adapta às mudanças do ambiente externo?",
    "Resiliência e Flexibilidade: Como a organização lida com crises e situações imprevistas?",
    "Segurança Cibernética: Como a organização trata a segurança cibernética em sua cultura?",
    "Medição da Cultura Digital: Como a organização mede e avalia o progresso da cultura digital?",
    "Autonomia e Empowerment: Como a organização promove a autonomia e o empowerment dos colaboradores na era digital?",
    "Gestão do Conhecimento Digital: Qual é a abordagem da organização em relação à gestão do conhecimento digital?",
    "Integração de Tecnologias Emergentes: Como a organização integra tecnologias emergentes em sua cultura?",
    "Envolvimento de Clientes e Parceiros: Como a organização envolve clientes e parceiros no desenvolvimento digital?",
    "Atitude em Relação ao Risco: Qual é a atitude da organização em relação ao risco e à falha em iniciativas digitais?",
    "Alinhamento Estratégico: Como a organização alinha sua estratégia digital com os valores e objetivos corporativos?",
    "Inovação Digital: Como a organização incentiva a inovação e a experimentação digital?",
    "Metodologias Ágeis: De que forma a organização integra práticas ágeis em seus processos?",
    "Diversidade e Inclusão: Como a organização promove a diversidade e inclusão em seu ambiente de trabalho?"
]

# Função para gerar o feedback via OpenAI
def generate_feedback(responses):
    prompt = "Com base nas seguintes respostas numéricas de 1 a 6, onde 1 significa que a cultura é fraca na questão e 6 significa que a cultura é forte, gere no formato markdown os pontos fortes e pontos a melhorar da empresa em relação à cultura organizacional:\n\n"
    for i, response in enumerate(responses):
        prompt += f"{perguntas[i]} Resposta: {response}/6\n"
    prompt += "\nBaseado nessas respostas, forneça os principais pontos fortes e os principais pontos de melhoria na cultura organizacional desta empresa."
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um consultor de cultura organizacional e transformação digital."},
                {"role": "user", "content": prompt}
            ]
        )
        # Extrair o conteúdo gerado pela OpenAI
        feedback = response.choices[0].message["content"].strip()
        return feedback
    except Exception as e:
        return f"Erro ao gerar feedback: {str(e)}"

# Função principal para carregar e exibir os resultados
def page_results():
    st.title("Resultados das Avaliações de Maturidade")

    # Carregar os resultados das empresas do CSV do GitHub
    try:
        df = load_responses_csv()
    except:
        st.error("Erro ao carregar o arquivo de resultados.")
        return

    empresa_selecionada = st.selectbox("Selecione a empresa para ver o resultado:", df["Empresa"].unique())
    resultado_empresa = df[df["Empresa"] == empresa_selecionada].iloc[0]
    maturity_index = resultado_empresa["Indice_Maturidade"]
    responses = eval(resultado_empresa["Respostas"])

    display_bars(maturity_index)

    st.write("**Feedback personalizado (via OpenAI):**")
    feedback = generate_feedback(responses)
    st.markdown(feedback)

if __name__ == "__main__":
    page_results()











