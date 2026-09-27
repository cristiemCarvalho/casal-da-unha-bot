import os

import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

st.set_page_config(
    page_title="Chat Casal da Unha",
    page_icon="💅",
    layout="centered",
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #FAFAFA;
    }

    h1 {
        color: #E8A7A1 !important;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
    }

    .stButton > button {
        background-color: #D4AF37 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
    }

    .stChatMessage {
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
if os.path.exists(logo_path):
    try:
        st.image(logo_path, use_container_width=True)
    except Exception as error:
        st.warning(f"Não foi possível carregar o logótipo: {error}")
else:
    st.warning("Logótipo não encontrado. A carregar aplicação...")

st.title("💅 NailPrecifica - Casal da Unha")
st.caption(
    "Olá! ✨ Seja muito bem-vinda ao Chat do Casal da Unha! 💅 "
    "Sou a assistente virtual da Instrutora Bia e estou aqui para te ajudar "
    "a descomplicar as suas contas, valorizar o seu trabalho em mesa e lotar "
    "a sua agenda! 🚀 Como posso te ajudar a decolar hoje?"
)

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except (KeyError, StreamlitSecretNotFoundError):
    api_key = None
except Exception as error:
    st.error(f"Não foi possível ler os Secrets do Streamlit: {error}")
    st.stop()

if not api_key:
    api_key = os.getenv("GOOGLE_API_KEY")

if isinstance(api_key, str):
    api_key = api_key.strip()
else:
    api_key = None

if not api_key:
    st.error("⚠️ Chave GOOGLE_API_KEY não encontrada.")
    st.info(
        "Configura a chave em Settings > Secrets com a estrutura: "
        "GOOGLE_API_KEY = 'tua_chave'"
    )
    st.stop()

try:
    from google import genai

    client = genai.Client(api_key=api_key)
except Exception as error:
    st.error(f"Erro ao inicializar o cliente Gemini: {error}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Como posso ajudar com a precificação hoje?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
            )
            answer = response.text
            if not answer:
                st.error("O Gemini não devolveu uma resposta. Tenta novamente.")
            else:
                st.markdown(answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
        except Exception as error:
            st.error(
                "Erro ao obter resposta do Gemini. Verifica a ligação, "
                f"a chave e a quota da API. Detalhes: {error}"
            )
