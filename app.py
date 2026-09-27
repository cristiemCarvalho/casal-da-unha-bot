import os

import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

st.set_page_config(
    page_title="Casal da Unha Chatbot",
    page_icon="💅",
    layout="centered",
)

st.markdown(
    """
    <style>
    :root {
        --page-background: #fafafa;
        --chat-pink: #e8a7a1;
        --chat-pink-light: #fff1ef;
        --chat-ink: #302b28;
        --gold: #d4af37;
    }

    .stApp {
        background: var(--page-background);
        color: var(--chat-ink);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    .block-container {
        max-width: 850px;
        padding-top: 1.5rem;
        padding-bottom: 6rem;
    }

    .main-title {
        margin: 0 0 4px;
        color: #c87d87;
        font-size: 2.2rem;
        font-weight: 800;
        text-align: center;
    }

    .sub-title {
        margin: 0 0 25px;
        color: #666;
        font-size: 1rem;
        text-align: center;
    }

    .top-status-bar {
        display: flex;
        width: fit-content;
        align-items: center;
        justify-content: center;
        gap: 8px;
        margin: 0 auto 15px;
        padding: 6px 16px;
        border-radius: 20px;
        background: #f4eeea;
        color: #4a4a4a;
        font-size: 0.85rem;
        font-weight: 600;
    }

    .status-dot {
        display: inline-block;
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background: #2ecc71;
        box-shadow: 0 0 8px #2ecc71;
    }

    [data-testid="stChatMessage"] {
        max-width: 88%;
        margin-bottom: 14px;
        padding: 14px 18px;
        border: 1px solid #f0e6e6;
        border-radius: 16px;
        background: #fff;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    }

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        margin-left: auto;
        border-color: #f0ceca;
        background: var(--chat-pink-light);
    }

    [data-testid="stChatInput"] {
        border: 1px solid var(--chat-pink);
        border-radius: 20px;
        background: #fff;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.04);
    }

    [data-testid="stChatInput"] textarea {
        background: transparent;
    }

    div.stButton > button {
        width: 100%;
        padding: 10px 14px;
        border: none;
        border-radius: 20px;
        background: var(--gold);
        color: #fff;
        font-size: 0.88rem;
        font-weight: 600;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
        transition: all 0.25s ease-in-out;
    }

    div.stButton > button:hover {
        background: #c5a028;
        color: #fff;
        transform: scale(1.02);
    }

    [data-testid="stSidebar"] {
        background: #f6f1eb;
    }

    @media (max-width: 640px) {
        .block-container {
            padding: 1rem 0.8rem 5.5rem;
        }

        .main-title {
            font-size: 1.8rem;
        }

        [data-testid="stChatMessage"] {
            max-width: 95%;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

project_dir = os.path.dirname(os.path.abspath(__file__))
avatar_jpg = os.path.join(project_dir, "bia.jpg")
avatar_png = os.path.join(project_dir, "bia.png")
if os.path.exists(avatar_jpg):
    avatar_bia = avatar_jpg
elif os.path.exists(avatar_png):
    avatar_bia = avatar_png
else:
    avatar_bia = "💅"

st.markdown(
    """
    <div class="top-status-bar">
        <span class="status-dot"></span>
        Assistente virtual do Casal da Unha · online
    </div>
    """,
    unsafe_allow_html=True,
)
WELCOME_MESSAGE = (
    "Oii, maravilhosa! ✨ Seja muito bem-vinda ao **Casal da Unha**! 💅\n\n"
    "Tô aqui pra te ajudar a valorizar teu trabalho em mesa, organizar os "
    "lucros e fazer essa agenda florescer. Me conta: por onde começamos? 💖"
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
    st.caption("Dica de amiga: preço justo também é autocuidado com teu negócio. ✨")

logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
if os.path.exists(logo_path):
    try:
        logo_columns = st.columns([1, 1.8, 1])
        with logo_columns[1]:
            st.image(logo_path, use_container_width=True)
    except Exception as error:
        st.warning(f"Não foi possível carregar o logótipo: {error}")

st.markdown(
    '<h1 class="main-title">💅 Casal da Unha</h1>'
    '<p class="sub-title">Tua assistente inteligente de precificação e gestão '
    'no Casal da Unha ✨</p>',
    unsafe_allow_html=True,
)

PROMPT_SISTEMA_BIA = """
Você é a assistente virtual do Casal da Unha. Fale com a nail designer como
uma amiga próxima, carinhosa e experiente: alegre, motivadora, espontânea e
bem-humorada, com brincadeiras leves e respeitosas. Seja firme quando precisar
lembrar que trabalho profissional não é favor e não deve dar prejuízo.

Você é uma assistente virtual, não uma pessoa real, a Instrutora Bia Putinatti
ou a esposa de alguém. Não afirme ser nenhuma dessas pessoas.

Ajude nail designers, iniciantes ou experientes, a:
- precificar serviços considerando materiais, tempo de mesa, custos fixos e lucro;
- valorizar o próprio trabalho e cobrar com confiança;
- atrair e fidelizar clientes, organizar a agenda e gerir o studio.

Use português brasileiro natural, frases fáceis de ler no celular e emojis com
moderação. Seja didática e direta: explique os cálculos por etapas e use reais
(R$) nos exemplos. Pergunte pelos dados que faltarem em vez de inventar valores;
explique as hipóteses de qualquer estimativa e não prometa resultados garantidos.
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
    avatar = avatar_bia if message["role"] == "assistant" else "🌸"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

suggested_prompt = None
if len(st.session_state.messages) == 1:
    st.markdown("**💡 Dúvidas frequentes — escolhe uma pra gente começar:**")
    suggestion_columns = st.columns(2)
    suggestions = (
        (
            "📊 Como calcular preço do gel ou fibra?",
            "Me ajuda a calcular do zero quanto cobrar no alongamento em gel ou fibra?",
        ),
        (
            "💬 O que falar quando pedem desconto?",
            "Como responder com carinho e firmeza quando uma cliente pede desconto?",
        ),
        (
            "📅 Como atrair mais clientes?",
            "Quais estratégias práticas ajudam uma nail designer a atrair e fidelizar clientes?",
        ),
        (
            "💎 Quanto cobrar na manutenção?",
            "Quais custos e critérios devo considerar para calcular o preço da manutenção?",
        ),
    )
    for index, (label, question) in enumerate(suggestions):
        with suggestion_columns[index % 2]:
            if st.button(label, key=f"suggestion_{index}"):
                suggested_prompt = question

typed_prompt = st.chat_input("Escreve aqui tua dúvida... vamos resolver juntas 💬")
prompt = typed_prompt or suggested_prompt

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🌸"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=avatar_bia):
        history = []
        for message in st.session_state.messages:
            if message.get("is_welcome"):
                continue
            role = "model" if message["role"] == "assistant" else "user"
            if history and history[-1]["role"] == role:
                history[-1]["parts"].append({"text": message["content"]})
            else:
                history.append({"role": role, "parts": [{"text": message["content"]}]})
        history = history[-20:]
        if history and history[0]["role"] == "model":
            history = history[1:]

        config = types.GenerateContentConfig(
            system_instruction=PROMPT_SISTEMA_BIA,
            temperature=0.7,
        )
        models = ("gemini-3.8-flash", "gemini-3.7-flash", "gemini-2.5-flash")
        model_errors = []

        for model_name in models:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=history,
                    config=config,
                )
            except Exception as error:
                model_errors.append(f"{model_name}: {error}")
                continue

            answer = response.text
            if not answer:
                st.error(
                    f"O modelo {model_name} não devolveu uma resposta. "
                    "Tenta enviar de novo, tá? ✨"
                )
            else:
                st.markdown(answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
            break
        else:
            st.error(
                "Não consegui conectar a nenhum dos modelos disponíveis. "
                "Confere a ligação, a chave e a quota da API e tenta novamente."
            )
            with st.expander("Detalhes técnicos"):
                for model_error in model_errors:
                    st.write(model_error)
