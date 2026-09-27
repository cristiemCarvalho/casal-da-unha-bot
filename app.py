import os
import re
import unicodedata

import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError

st.set_page_config(
    page_title="Casal da Unha Chatbot | Assistente",
    page_icon="💅",
    layout="centered",
    initial_sidebar_state="collapsed",
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
        background: #fafaf8;
        color: var(--chat-ink);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    .block-container {
        max-width: 850px;
        padding-top: 1.5rem;
        padding-bottom: 6rem;
    }

    .hero-header {
        margin-bottom: 16px;
        padding: 16px 14px;
        border: 1px solid var(--gold);
        border-radius: 16px;
        background: linear-gradient(135deg, #1c1c1c 0%, #2d2522 100%);
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.12);
        text-align: center;
    }

    .hero-title {
        margin: 0 0 4px;
        color: #f3c5c5;
        font-size: 1.5rem;
        font-weight: 800;
    }

    .hero-subtitle {
        margin: 0;
        color: #e2c97e;
        font-size: 0.88rem;
        font-weight: 500;
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

    [data-testid="stChatMessage"],
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessageContent"] {
        color: #31333f !important;
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
        margin-bottom: 4px;
        padding: 10px 12px;
        border: 1.5px solid #e8d8ce;
        border-radius: 12px;
        background: #fff;
        color: #4a3b32;
        font-size: 0.88rem;
        font-weight: 600;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
    }

    div.stButton > button:hover,
    div.stButton > button:active {
        border-color: var(--gold);
        background: #fdf7f3;
        color: #4a3b32;
        transform: scale(0.98);
    }

    [data-testid="stSidebar"] {
        background: #f6f1eb;
    }

    [data-testid="stSidebar"],
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: #31333f !important;
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 1rem 0.8rem 5rem;
        }

        .hero-title {
            font-size: 1.3rem;
        }

        .hero-subtitle {
            font-size: 0.8rem;
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
    """
    <div class="hero-header">
        <div class="hero-title">✨ Chatbot Casal da Unha</div>
        <div class="hero-subtitle">
            Tua amiga das finanças, da mesa e da agenda cheia 24h 💅💎
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

PROMPT_SISTEMA_BIA = """
Você é a assistente virtual do Casal da Unha, com uma voz calorosa, alegre,
motivadora, empática e bem-humorada. Seja firme com carinho quando lembrar que
trabalho profissional não é favor e não deve dar prejuízo. Apresente-se como
assistente virtual; não afirme ser a pessoa real Bia Putinatti ou outra pessoa.

Ajude nail designers com precificação, custos de materiais e tempo de mesa,
cuidados gerais com unhas, técnicas de alongamento, organização do studio,
atração de clientes e gestão da agenda. Use português brasileiro natural,
respostas fáceis de ler no celular e emojis com moderação. Explique cálculos
passo a passo em reais (R$), pergunte os dados que faltarem e não invente fatos.

Referências técnicas fornecidas pelo Casal da Unha:
- Anatomia: lâmina e leito ungueal, matriz, lúnula, eponíquio, hiponíquio e
  pregas/sulcos laterais e proximais. Não confunda a cutícula solta com o
  eponíquio, que protege a região proximal.
- Na remoção, preserve a unha natural e não lixe até remover toda a placa ou
  causar dor, calor excessivo ou afinamento.
- Materiais incluem cabine UV/LED apropriada ao produto, micromotor, coletor de
  pó, iluminação e ferramentas adequadas. Siga sempre as instruções do fabricante
  para preparação, aplicação e tempo de cura; não presuma que um tempo único
  sirva para todos os produtos e equipamentos.
- Uma sequência geral de preparação e aplicação pode incluir higienização,
  preparação suave da lâmina, desidratação/primer quando indicados pelo sistema,
  base, construção, acabamento e selagem. Respeite o protocolo do fabricante.
- O lixamento técnico exige controle de laterais, ápice, simetria, borda livre,
  arco e espessura, sem comprometer a unha natural.
- Gel de construção: prepare a unha sem agredir a lâmina, aplique somente as
  camadas previstas pelo sistema do fabricante, mantenha o produto afastado da
  pele e faça a cura completa com uma lâmpada compatível. Estruture o ápice e
  laterais sem excesso de produto; interrompa se houver ardor, irritação ou
  reação e não use produto não curado sobre a pele.
- Esmaltação em gel: use produtos compatíveis entre si e com a cabine, aplique
  camadas finas conforme as instruções do fabricante, sele a borda livre quando
  indicado e evite contato com pele e cutículas. Não improvise tempos de cura;
  produto subcurado pode aumentar riscos de sensibilização.
- Biossegurança: higienize as mãos e a estação, use EPIs adequados, faça a
  limpeza dos instrumentos antes da esterilização e utilize embalagem e ciclo
  compatíveis com o material e com as instruções do fabricante da autoclave.
  Siga o ciclo validado e as exigências da vigilância sanitária local; registre
  ciclos e monitore indicadores conforme o protocolo aplicável. Não trate
  desinfecção como sinônimo de esterilização nem reutilize itens descartáveis.
- Cursos: não invente preços, datas, vagas, certificados ou conteúdo não
  confirmado. Oriente a consultar o canal oficial do Casal da Unha para a tabela
  e as condições atualizadas dos cursos presenciais.
- Os intervalos de manutenção dependem do crescimento, condição e estrutura:
  clientes com unhas roídas, úmidas ou de maior impacto podem precisar de
  avaliação e retorno antes. Não apresente prazo como regra médica universal.

Não diagnostique doenças nem recomende tratar alterações suspeitas com produto
ou procedimento estético. Se houver dor, inflamação, descolamento, mudança de
cor ou suspeita de infecção/alergia, oriente interromper o procedimento e buscar
avaliação de profissional de saúde qualificado.
"""

RESPOSTAS_RAPIDAS_LOCAIS = (
    (
        (
            "preco do curso",
            "preco dos cursos",
            "valor do curso",
            "valor dos cursos",
            "curso presencial",
            "cursos presenciais",
        ),
        "📚 Os valores, datas e vagas dos cursos podem mudar. Não tenho uma "
        "tabela atualizada confirmada; consulta o canal oficial do Casal da "
        "Unha para receber preços e condições corretos.",
    ),
    (
        ("biosseguranca", "autoclave", "esterilizacao", "esterilizar instrumento"),
        "🧼 **Biossegurança:** primeiro faça a limpeza correta dos instrumentos; "
        "depois use embalagem e ciclo de autoclave compatíveis com o material, "
        "seguindo o manual do equipamento e as regras da vigilância sanitária "
        "local. Registre os ciclos e use os indicadores previstos no protocolo. "
        "Desinfecção não é o mesmo que esterilização, e itens descartáveis não "
        "devem ser reutilizados. Não existe um tempo/temperatura único para "
        "todas as autoclaves e cargas.",
    ),
    (
        ("gel de construcao", "gel construtor", "construcao em gel"),
        "💅 **Gel de construção:** segue o sistema completo indicado pelo "
        "fabricante: preparação suave, produtos compatíveis, camadas e cura "
        "conforme o rótulo e a cabine. Mantenha o gel longe da pele e estruture "
        "ápice e laterais sem excesso. Não há um tempo de cura universal; "
        "produto subcurado ou em contato com a pele pode causar sensibilização.",
    ),
    (
        ("esmalte em gel", "esmaltacao em gel", "esmalte gel", "esmaltacao gel"),
        "✨ **Esmaltação em gel:** use base, cor, top coat e cabine compatíveis. "
        "Aplique camadas finas, evite tocar pele e cutículas e respeite os tempos "
        "de cura do fabricante para cada produto e lâmpada. Não tente compensar "
        "incompatibilidade ou camada grossa aumentando o tempo por conta própria.",
    ),
    (
        ("manutencao", "manutencoes", "prazo de manutencao", "quando fazer manutencao"),
        "💅 **Manutenção:** como referência informada pelo Casal da Unha, "
        "o retorno costuma ser avaliado entre 15 e 21 dias; em unhas roídas, "
        "úmidas ou de maior impacto, pode ser necessário reavaliar entre 7 e "
        "14 dias. O intervalo depende da condição da unha, do produto e da "
        "avaliação profissional. Se houver dor ou alteração suspeita, não "
        "faça cobertura estética: procure avaliação de saúde.",
    ),
    (
        ("preco", "precos", "valor", "valores", "quanto cobrar"),
        "💰 Para consultar a tabela atualizada de atendimentos e cursos do "
        "Casal da Unha, envia uma mensagem diretamente pelo WhatsApp oficial. "
        "Para calcular o preço do teu próprio serviço, também posso te ajudar "
        "a levantar material, tempo de mesa, custos fixos e lucro.",
    ),
    (
        ("horario", "horarios", "que horas atende", "horario de atendimento"),
        "⏰ O horário informado pelo Casal da Unha é de segunda a sábado, "
        "das 08h às 19h, com agendamento prévio. Confirma a disponibilidade "
        "pelo canal oficial antes de se deslocar.",
    ),
    (
        ("pincel", "pinceis"),
        "🖌️ **Pincéis:** a referência do Casal da Unha indica o língua de "
        "gato de 8 mm para gel base e o chanfrado de 7 mm para gel construtor. "
        "A escolha também depende da viscosidade do produto e da técnica.",
    ),
    (
        ("broca", "brocas", "anel de corte"),
        "💎 **Anéis de corte das brocas — referência geral:**\n"
        "- Amarelo: extra fina\n- Vermelho: fina\n- Azul: média\n"
        "- Verde: grossa\n- Preto: extra grossa\n\n"
        "A abrasividade varia conforme a broca. Escolhe a ferramenta e a "
        "pressão conforme a área e a formação profissional; evita trabalhar "
        "sobre a unha natural de forma agressiva.",
    ),
)


def normalizar_texto(texto):
    texto_sem_acentos = unicodedata.normalize("NFKD", texto)
    return "".join(
        caractere
        for caractere in texto_sem_acentos
        if not unicodedata.combining(caractere)
    ).casefold()


def consultar_resposta_local(texto):
    texto_normalizado = " ".join(
        re.findall(r"\w+", normalizar_texto(texto), flags=re.UNICODE)
    )
    palavras = set(texto_normalizado.split())
    for termos, resposta in RESPOSTAS_RAPIDAS_LOCAIS:
        if any(
            termo in palavras or f" {termo} " in f" {texto_normalizado} "
            for termo in termos
        ):
            return resposta
    return None


try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except (KeyError, StreamlitSecretNotFoundError):
    api_key = None
except Exception as error:
    st.error(f"Não foi possível ler os Secrets do Streamlit: {error}")
    api_key = None

if not api_key:
    api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    api_key = os.getenv("GEMINI_API_KEY")

if isinstance(api_key, str):
    api_key = api_key.strip()
else:
    api_key = None

client = None
client_error = None
types = None
try:
    if api_key:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
except Exception as error:
    client_error = str(error)

if not client:
    st.info(
        "As respostas rápidas continuam disponíveis. Para perguntas abertas, "
        "configura GOOGLE_API_KEY nos Secrets do Streamlit ou define-a como "
        "variável de ambiente."
    )
    if client_error:
        st.warning(f"Não foi possível inicializar o Gemini: {client_error}")

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
        resposta_local = consultar_resposta_local(prompt)
        if resposta_local:
            st.markdown(resposta_local)
            st.session_state.messages.append(
                {"role": "assistant", "content": resposta_local}
            )
        elif not client or not types:
            st.error(
                "Não consigo responder a essa pergunta sem o Gemini. "
                "As respostas rápidas continuam disponíveis; configura uma "
                "chave válida para perguntas abertas."
            )
        else:
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

            config = types.GenerateContentConfig(
                system_instruction=PROMPT_SISTEMA_BIA,
                temperature=0.7,
            )
            models = (
                "gemini-3.8-flash",
                "gemini-2.5-flash",
            )
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

                answer = response.text if response else None
                if not answer:
                    model_errors.append(f"{model_name}: resposta sem texto")
                    continue

                st.markdown(answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
                break
            else:
                st.error(
                    "Não foi possível obter uma resposta. Pode ser uma "
                    "instabilidade ou um limite temporário de quota; aguarda "
                    "um minuto e tenta de novo. Se continuar, verifica a chave "
                    "e os detalhes técnicos abaixo."
                )
                with st.expander("Detalhes técnicos"):
                    for model_error in model_errors:
                        st.write(model_error)
