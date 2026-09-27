import os

import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

st.set_page_config(
    page_title="Casal da Unha | NailPrecifica",
    page_icon="💅",
    layout="centered",
)

st.markdown(
    """
    <style>
    :root {
        --chat-green: #075e54;
        --chat-green-light: #d9fdd3;
        --chat-background: #efeae2;
        --chat-ink: #25332f;
    }

    .stApp {
        background: var(--chat-background);
        color: var(--chat-ink);
    }

    .block-container {
        max-width: 850px;
        padding-top: 1.5rem;
        padding-bottom: 6rem;
    }

    .chat-header {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 1.25rem;
        padding: 16px 20px;
        border-radius: 18px;
        background: var(--chat-green);
        color: #fff;
        box-shadow: 0 4px 14px rgba(27, 54, 47, 0.12);
    }

    .chat-header__avatar {
        display: grid;
        width: 48px;
        height: 48px;
        flex: 0 0 48px;
        place-items: center;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.16);
        font-size: 1.55rem;
    }

    .chat-header__title {
        margin: 0;
        color: #fff;
        font-size: 1.18rem;
        font-weight: 700;
    }

    .chat-header__status {
        margin: 3px 0 0;
        color: #d6eee9;
        font-size: 0.88rem;
    }

    [data-testid="stChatMessage"] {
        max-width: 88%;
        margin-bottom: 12px;
        padding: 12px 16px;
        border: 1px solid #e7e1d7;
        border-radius: 17px;
        background: #fff;
        box-shadow: 0 2px 7px rgba(42, 54, 48, 0.06);
    }

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        margin-left: auto;
        border-color: #c6e8bd;
        background: var(--chat-green-light);
    }

    [data-testid="stChatInput"] {
        border-color: #c7d8cf;
        border-radius: 18px;
        background: #fff;
    }

    [data-testid="stChatInput"] textarea {
        background: transparent;
    }

    [data-testid="stChatInput"] button {
        color: var(--chat-green);
    }

    [data-testid="stSidebar"] {
        background: #f8f5ef;
    }

    @media (max-width: 640px) {
        .block-container {
            padding: 1rem 0.8rem 5.5rem;
        }

        [data-testid="stChatMessage"] {
            max-width: 95%;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

WELCOME_MESSAGE = (
    "Oii, maravilhosa! ✨ Que bom te ver por aqui. Vamos cuidar dos números "
    "do teu negócio e fazer essa agenda brilhar? Me conta: no que posso te "
    "dar uma mão hoje? 💅"
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": WELCOME_MESSAGE, "is_welcome": True}
    ]

with st.sidebar:
    st.markdown("### 💅 Casal da Unha")
    st.caption("Um cantinho para cuidar dos números e fazer a agenda florescer.")
    if st.button("＋ Nova conversa", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": WELCOME_MESSAGE, "is_welcome": True}
        ]
        st.rerun()
    st.divider()
    st.caption("Dica de amiga: preço justo também é autocuidado com o teu negócio. ✨")

logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
if os.path.exists(logo_path):
    try:
        st.image(logo_path, width=140)
    except Exception as error:
        st.warning(f"Não foi possível carregar o logótipo: {error}")

st.markdown(
    """
    <div class="chat-header">
        <div class="chat-header__avatar">💅</div>
        <div>
            <p class="chat-header__title">NailPrecifica</p>
            <p class="chat-header__status">Assistente do Casal da Unha · pronta pra conversar ✨</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

PROMPT_SISTEMA_BIA = """
Você é a assistente virtual do Casal da Unha, com uma voz próxima e acolhedora,
inspirada numa parceira carinhosa que conversa com a nail designer no dia a dia.
Apresente-se como assistente virtual; não afirme ser uma pessoa real, a Instrutora
Bia ou a esposa de alguém.

Seu objetivo é ajudar nail designers a:
- calcular preços considerando materiais, tempo de mesa, custos fixos e lucro;
- valorizar o próprio trabalho e cobrar com confiança;
- organizar o studio, atrair clientes e fidelizar quem já está na agenda.

Personalidade: alegre, calorosa, motivadora e espontânea, com brincadeiras leves
e respeitosas. Seja carinhosa sem exagerar, e firme quando precisar lembrar que
trabalho profissional não é favor nem deve dar prejuízo. Use português brasileiro
natural, frases fáceis de ler no celular e emojis com moderação.

Ao ajudar com precificação, explique as contas de forma clara. Pergunte pelos
dados que faltarem em vez de inventar valores. Deixe explícitas as hipóteses de
qualquer estimativa e não prometa resultados garantidos para o negócio.
"""

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
        "Adiciona GOOGLE_API_KEY aos Secrets do Streamlit Cloud ou define-a "
        "como variável de ambiente."
    )
    st.stop()

try:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
except Exception as error:
    st.error(f"Não foi possível inicializar o cliente Gemini: {error}")
    st.stop()

for message in st.session_state.messages:
    avatar = "💅" if message["role"] == "assistant" else "🌸"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

quick_prompt = None
if len(st.session_state.messages) == 1:
    st.markdown("**Por onde a gente começa?**")
    prompt_columns = st.columns(3)
    quick_prompts = (
        "💰 Quero calcular o preço de um serviço",
        "📊 Me ajuda a organizar meus custos",
        "✨ Como posso atrair mais clientes?",
    )
    for column, suggestion in zip(prompt_columns, quick_prompts):
        with column:
            if st.button(suggestion, use_container_width=True):
                quick_prompt = suggestion.split(" ", 1)[1]

submitted_prompt = st.chat_input("Escreve aqui... vamos resolver juntas 💬")
prompt = submitted_prompt or quick_prompt

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🌸"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="💅"):
        try:
            history = []
            for message in st.session_state.messages:
                if message.get("is_welcome"):
                    continue
                role = "model" if message["role"] == "assistant" else "user"
                if history and history[-1]["role"] == role:
                    history[-1]["parts"].append({"text": message["content"]})
                else:
                    history.append(
                        {"role": role, "parts": [{"text": message["content"]}]}
                    )
            history = history[-20:]
            if history and history[0]["role"] == "model":
                history = history[1:]

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=history,
                config=types.GenerateContentConfig(
                    system_instruction=PROMPT_SISTEMA_BIA,
                    temperature=0.7,
                ),
            )
            answer = response.text
            if not answer:
                st.error("Não veio uma resposta desta vez. Tenta de novo, tá? ✨")
            else:
                st.markdown(answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
        except Exception as error:
            st.error(
                "Não consegui buscar a resposta agora. Confere a ligação, "
                "a chave e a quota da API e tenta novamente. "
                f"Detalhes: {error}"
            )
