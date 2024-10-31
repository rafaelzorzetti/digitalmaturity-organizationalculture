import streamlit as st
from github import Github
import os

# Configurar o token de acesso pessoal (PAT) e o repositório
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
REPO_NAME = "rafaelzorzetti/digitalmaturity-organizationalculture"
IMAGE_FOLDER_PATH = "views/"  # Caminho da pasta onde as imagens serão salvas
MARKDOWN_FILE_PATH = "views/intro.md"  # Caminho do arquivo markdown

# Função para salvar a imagem no GitHub corretamente
def save_image_to_github(image_file, image_name, commit_message="Adicionando imagem"):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    # Abrir a imagem como binário
    image_content = image_file.getvalue()

    # Caminho do arquivo no repositório
    image_path = f"{IMAGE_FOLDER_PATH}{image_name}"

    try:
        # Tentar obter o conteúdo atual do arquivo (se ele já existir)
        file_content = repo.get_contents(image_path)
        # Atualizar o arquivo existente
        repo.update_file(file_content.path, commit_message, image_content, file_content.sha)
    except:
        # Se o arquivo não existir, criar um novo
        repo.create_file(image_path, commit_message, image_content)

    # Retornar o caminho da imagem no GitHub
    return f"https://raw.githubusercontent.com/{REPO_NAME}/main/{image_path}"

# Função para salvar o markdown atualizado no GitHub
def save_markdown_file_to_github(content, commit_message="Atualizando arquivo de introdução"):
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

# Página de introdução no Streamlit
def page_intro():
    st.title("Introdução")

    # Carregar o conteúdo atual do markdown
    markdown_content = read_markdown_file(MARKDOWN_FILE_PATH)

    # Exibir o conteúdo atual do markdown
    st.markdown(markdown_content)

    if st.session_state.get('logged_in'):
    
        # Exibir caixa de texto para o usuário editar o markdown
        st.write("### Modificar o conteúdo abaixo:")
        updated_content = st.text_area("Editar introdução", markdown_content, height=300)

        # Upload de imagem
        uploaded_image = st.file_uploader("Carregar uma imagem", type=["png", "jpg", "jpeg"])
        
        # Se uma imagem for carregada, salvar no GitHub e gerar o caminho da imagem
        if uploaded_image is not None:
            image_name = uploaded_image.name
            image_url = save_image_to_github(uploaded_image, image_name)
            
            # Adicionar o caminho da imagem ao markdown
            updated_content += f"\n\n![Imagem carregada]({image_url})"
        
        # Botão para salvar as alterações
        if st.button("Salvar Alterações"):
            # Salvar o conteúdo atualizado no markdown no GitHub
            save_markdown_file_to_github(updated_content)
            
            # Recarregar o conteúdo atualizado
            st.success("Alterações salvas com sucesso!")
            st.rerun()

# Chamar a função na página principal
if __name__ == "__main__":
    page_intro()





