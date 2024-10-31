import streamlit as st
from github import Github
import os

# Configurar o token de acesso pessoal (PAT) e o repositório
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
REPO_NAME = "rafaelzorzetti/digitalmaturity-organizationalculture"
MARKDOWN_FILE_PATH = "views/avaliacao_maturidade.md"  # Caminho do arquivo markdown

# Função para salvar o markdown atualizado no GitHub
def save_markdown_file_to_github(content, commit_message="Atualizando arquivo de Avaliação da Maturidade"):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    file_content = repo.get_contents(MARKDOWN_FILE_PATH)
    repo.update_file(file_content.path, commit_message, content, file_content.sha)

# Função para ler o arquivo markdown do GitHub
def read_markdown_file(file_path):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    file_content = repo.get_contents(file_path)
    return file_content.decoded_content.decode('utf-8')

# Página de Avaliação da Maturidade no Streamlit
def page_avaliacao_maturidade():
    st.title("Avaliação da Maturidade da Cultura Organizacional")

    # Carregar o conteúdo atual do markdown
    markdown_content = read_markdown_file(MARKDOWN_FILE_PATH)

    # Exibir o conteúdo atual do markdown
    st.markdown(markdown_content)
    
    if st.session_state.get('logged_in'):
        
        # Exibir caixa de texto para o usuário editar o markdown
        st.write("### Modificar o conteúdo abaixo:")
        updated_content = st.text_area("Editar Avaliação da Maturidade", markdown_content, height=300)

        # Botão para salvar as alterações
        if st.button("Salvar Alterações"):
            # Salvar o conteúdo atualizado no markdown no GitHub
            save_markdown_file_to_github(updated_content)
            
            # Recarregar o conteúdo atualizado
            st.success("Alterações salvas com sucesso!")
            st.rerun()

# Chamar a função na página principal
if __name__ == "__main__":
    page_avaliacao_maturidade()

