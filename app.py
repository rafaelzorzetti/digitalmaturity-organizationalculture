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
    
    #Carrega a imagem do side bar
    logo_path = os.path.join('usjt_logo.jpg')  # Caminho para o logo
    st.sidebar.image(logo_path, use_column_width=True)
    
    st.sidebar.title("Login")
    
    # Entrada de nome de usuário
    username = st.sidebar.text_input("Usuário")
    # Entrada de senha
    password = st.sidebar.text_input("Senha", type="password")
    
    if st.sidebar.button("Login"):
        if username in USERS and check_password(password, USERS[username]):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.sidebar.success(f"Bem-vindo, {username}!")
            # Recarrega a página imediatamente após o login bem-sucedido
            st.rerun()
        else:
            st.sidebar.error("Usuário ou senha incorretos")

# Função de logout
def logout():
    st.session_state.clear()  # Limpar a sessão
    st.rerun()   # Recarregar a aplicação sem ser dentro do callback

# Função para limpar sessão (logout)
def clear_session():
    st.session_state.clear()
    st.rerun()  # Forçar recarregamento após o logout

# Função principal com autenticação
def main():
    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        # Cabeçalho principal com o título e a lista de participantes, sempre visível

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

    if st.session_state['logged_in']:
        with st.sidebar:
            
            #Carrega a imagem do side bar
            logo_path = os.path.join('usjt_logo.jpg')  # Caminho para o logo
            st.image(logo_path, use_column_width=True)

            selected = option_menu(
                menu_title="Navegação",
                options=["Introdução", "Fundamentos Teóricos", "Avaliação da Maturidade", "Questionário", "Resultados", "Conclusão", "Referências", "Sair"]
            )

        # Navegação para as páginas
        if selected == "Introdução":
            intro.page_intro()
        if selected == "Fundamentos Teóricos":
            fundamentos_teoricos.page_fundamentos_teoricos()
        if selected == "Avaliação da Maturidade":
            avaliacao_maturidade.page_avaliacao_maturidade()
        if selected == "Questionário":
            questonario.page_questionnaire()
        if selected == "Resultados":
            resultados.page_results()
        if selected == "Conclusão":
            conclusao.page_conclusao()
        if selected == "Referências":
            referencias.page_referencias()
        elif selected == "Sair":
            logout()
    else:
        login()

if __name__ == "__main__":
    main()