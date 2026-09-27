import os

import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

st.set_page_config(
    page_title="Casal da Unha - NailPrecifica",
    page_icon="💅",
    layout="centered",
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
    st.error("⚠️ A chave GOOGLE_API_KEY não foi configurada.")
    st.info(
        "Adiciona GOOGLE_API_KEY aos Secrets do Streamlit Cloud ou "
        "define-a como variável de ambiente."
    )
    st.stop()

try:
    import google.generativeai as genai

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as error:
    st.error(f"Não foi possível inicializar o Gemini: {error}")
    st.stop()

st.markdown("---")

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
            response = model.generate_content(prompt)
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
                "Não foi possível obter uma resposta do Gemini. "
                f"Verifica a ligação, a chave e a quota da API. Detalhes: {error}"
            )
