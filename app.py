import streamlit as st
from streamlit_option_menu import option_menu
from views import intro, avaliacao_maturidade, questonario, resultados, referencias, conclusao, fundamentos_teoricos
import bcrypt
import os

# Função para verificar o login
def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# Função para criar a senha hash
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Lista de usuários e senhas (exemplo simples)
USERS = {
    "admin": hash_password("admin123"),
}

# Função de login
def login():
    st.sidebar.title("Login")
    
    username = st.sidebar.text_input("Usuário")
    password = st.sidebar.text_input("Senha", type="password")
    
    if st.sidebar.button("Login"):
        if username in USERS and check_password(password, USERS[username]):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.sidebar.success(f"Bem-vindo, {username}!")
            st.rerun()
        else:
            st.sidebar.error("Usuário ou senha incorretos")

# Função de logout
def logout():
    st.session_state.clear()  # Limpa todo o estado da sessão
    st.session_state['logged_in'] = False  # Define como deslogado
    st.session_state['first_run'] = True  # Define para exibir a tela de participantes na próxima vez
    st.rerun()  # Força a recarga da aplicação

# Função principal com autenticação
def main():
    # Verificar se o usuário está logado
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    # Controle para exibir a tela de participantes na inicialização
    if 'first_run' not in st.session_state:
        st.session_state['first_run'] = True

    # Menu de navegação lateral
    with st.sidebar:
        logo_path = os.path.join('usjt_logo.jpg')
        st.image(logo_path, use_column_width=True)

        # Menu com as opções
        selected = option_menu(
            menu_title="Navegação",
            options=["Participantes", "Introdução", "Fundamentos Teóricos", "Avaliação da Maturidade", "Questionário", "Resultados", "Conclusão", "Referências", "Sair"],
            default_index=0
        )

    # Exibir a tela de participantes na inicialização ou após logout
    if selected == "Participantes" or st.session_state.get('first_run', False):
        st.session_state['first_run'] = False  # Garante que a tela de participantes só apareça uma vez
        st.markdown("## Projeto A3 da UC Aspectos Humanos e Socioculturais")
        st.markdown("## Índice de Maturidade da Cultura Organizacional para a Transformação Digital")
        st.markdown("""
        **Orientação:** Professora Sthael Ramos Silva 
        
        **RA/Matrícula e Nome Completo:**
        - 821119440: Alesi Moisés Ferreira Bueno
        - 821118671: Bruna Cristina dos Santos
        - 821134928: Isabela Bastos Neves
        - 82118366: Lucas Alexandre de Lima Santana
        - 821141677: Nathalia Storaro da Costa
        - 821128705: Rafael Zorzetti Pereira
        - 821130665: Sérgio Vinícius Matos de Azevedo
        - 82116865: Thais Silva Terruya
        - 821150801: Malcon Felipe Ribeiro
        - 821132677: Gustavo Nascimento Marianno Mendes
        """)
        # Exibir a tela de login se não estiver logado
        if not st.session_state['logged_in']:
            login()
            
        # Interrompe o restante do código, exibindo só a tela de participantes
        return

    # Navegação para as páginas de conteúdo
    elif selected == "Introdução":
        intro.page_intro()
    elif selected == "Fundamentos Teóricos":
        fundamentos_teoricos.page_fundamentos_teoricos()
    elif selected == "Avaliação da Maturidade":
        avaliacao_maturidade.page_avaliacao_maturidade()
    elif selected == "Questionário":
        questonario.page_questionnaire()
    elif selected == "Resultados":
        resultados.page_results()
    elif selected == "Conclusão":
        conclusao.page_conclusao()
    elif selected == "Referências":
        referencias.page_referencias()
    elif selected == "Sair":
        logout()  # Chama a função de logout, que limpa o estado e recarrega a aplicação

    # Exibir a tela de login se não estiver logado
    if not st.session_state['logged_in']:
        login()

if __name__ == "__main__":
    main()