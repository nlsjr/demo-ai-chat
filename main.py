import streamlit as st

from utils_openai import get_response
from utils_files import generate_uuid
from message_repository import read_distinct_chats, get_message_by_chat_id, create_message_by_chat_id


# INICIALIZAÇÃO ==================================================
def inicializacao():
    if not 'mensagens_tab' in st.session_state:
        st.session_state.mensagens_tab = []
    if not 'mensagens_conversa' in st.session_state:
        st.session_state.mensagens_conversa = []
    if not 'conversa_atual' in st.session_state:
        st.session_state.conversa_atual = ''


# TABS ==================================================
def tab_conversas(tab):
    tab.button('➕ Nova conversa',
               on_click=seleciona_conversa,
               args=('',),
               disabled=st.session_state['conversa_atual'] == '',
               use_container_width=True)
    tab.markdown('')
    conversas = read_distinct_chats()
    for conversa in conversas:
        read_conversas = get_message_by_chat_id(conversa['chat_id'])

        # Cria um iterador a partir da lista read_conversas
        iter_conversas = iter(read_conversas)

        # Obtém o primeiro item do iterador
        read_conversa = next(iter_conversas, None)

        nome_mensagem = read_conversa['content'].capitalize()
        if len(nome_mensagem) == 30:
            nome_mensagem += '...'
        tab.button(nome_mensagem,
                   on_click=seleciona_conversa,
                   args=(read_conversa['chat_id'],),
                   disabled=conversa['chat_id'] == st.session_state['conversa_atual'],
                   use_container_width=True)


def seleciona_conversa(chat_id):
    if chat_id == '':
        st.session_state['mensagens_conversa'] = []
    else:
        mensagens = get_message_by_chat_id(chat_id)
        st.session_state['mensagens_conversa'] = mensagens
    st.session_state['conversa_atual'] = chat_id


def tab_configuracoes(tab):
    modelo_escolhido = tab.selectbox('Selecione o modelo',
                                     ['gpt-3.5-turbo', 'gpt-4'])
    st.session_state['modelo'] = modelo_escolhido


def pagina_principal():
    mensagens = st.session_state['mensagens_conversa']
    conversa_atual = str(generate_uuid()) if st.session_state['conversa_atual'] == '' else st.session_state[
        'conversa_atual']

    st.header('🤖 Demo Chatbot', divider=True)

    for mensagem in mensagens:
        chat = st.chat_message(mensagem['role'])
        chat.markdown(mensagem['content'])

    prompt = st.chat_input('Fale com o chat')
    if prompt:
        nova_mensagem = {'role': 'human', 'content': prompt}

        chat = st.chat_message(nova_mensagem['role'])
        chat.markdown(nova_mensagem['content'])
        mensagens.append(nova_mensagem)
        create_message_by_chat_id(conversa_atual, nova_mensagem['role'], nova_mensagem['content'])

        chat = st.chat_message('ai')
        placeholder = chat.empty()
        placeholder.markdown("▌")
        resposta_completa = ''
        resposta = get_response(mensagens)

        resposta_completa += resposta['content']
        placeholder.markdown(resposta_completa + "▌")
        placeholder.markdown(resposta_completa)

        nova_mensagem = {'role': 'ai', 'content': resposta_completa}
        mensagens.append(nova_mensagem)

        st.session_state['mensagens_conversa'] = mensagens
        create_message_by_chat_id(conversa_atual, nova_mensagem['role'], nova_mensagem['content'])
        st.session_state['conversa_atual'] = conversa_atual


# MAIN ==================================================
def main():
    inicializacao()
    pagina_principal()
    tab1 = st.sidebar.tabs(['Conversas'])[0]
    tab_conversas(tab1)


if __name__ == '__main__':
    main()
