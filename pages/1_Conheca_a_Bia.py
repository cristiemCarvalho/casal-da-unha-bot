import os

import streamlit as st

st.set_page_config(
    page_title="Conheça a Bia | Casal da Unha",
    page_icon="💅",
    layout="centered",
)

st.markdown(
    """
    <style>
    .stApp {
        background: #faf8f6;
        color: #302b28;
    }

    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    .landing-hero {
        padding: 2rem 1.5rem;
        border: 1px solid #d4af37;
        border-radius: 22px;
        background: linear-gradient(135deg, #2d2522, #4a3036);
        color: #fff;
        text-align: center;
    }

    .landing-hero h1 {
        margin-bottom: 0.5rem;
        color: #f3c5c5;
        font-size: clamp(2rem, 7vw, 3.2rem);
    }

    .landing-hero p {
        color: #fff;
        font-size: 1.08rem;
    }

    .feature-card {
        height: 100%;
        padding: 1.1rem;
        border: 1px solid #f0e6e6;
        border-radius: 16px;
        background: #fff;
    }

    @media (max-width: 640px) {
        .block-container {
            padding: 1rem 0.8rem 3rem;
        }

        .landing-hero {
            padding: 1.5rem 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logo_path = os.path.join(project_dir, "logo.png")
if os.path.exists(logo_path):
    try:
        logo_columns = st.columns([1, 1.5, 1])
        with logo_columns[1]:
            st.image(logo_path, width="stretch")
    except Exception as error:
        st.warning(f"Não foi possível carregar o logótipo: {error}")

st.markdown(
    """
    <section class="landing-hero">
        <h1>💅 Conheça a Bia</h1>
        <p><strong>Uma assistente virtual do Casal da Unha para acompanhar
        a tua jornada como nail designer.</strong></p>
        <p>Técnicas, organização e aquela força amiga para valorizar
        o teu trabalho — numa conversa simples e acolhedora.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

st.write("")
st.link_button(
    "💬 Conversar com a assistente",
    "/",
    width="stretch",
)
st.caption(
    "Podes abrir o chat quando quiseres. As respostas com inteligência "
    "artificial dependem da disponibilidade do serviço."
)

st.subheader("Uma ajuda para a rotina do teu studio")
feature_columns = st.columns(3)
features = (
    (
        "🧪 Técnicas",
        "Tira dúvidas gerais sobre gel de construção, esmaltação em gel, "
        "manutenção e fundamentos de alongamento.",
    ),
    (
        "🧼 Biossegurança",
        "Revê princípios de higiene, limpeza e esterilização responsável, "
        "respeitando o manual dos equipamentos e as regras locais.",
    ),
    (
        "📚 Cursos e carreira",
        "Conversa sobre desenvolvimento profissional. Para preços, datas "
        "e vagas atualizados, consulta os canais oficiais do Casal da Unha.",
    ),
)
for column, (title, description) in zip(feature_columns, features):
    with column:
        st.markdown(
            f'<div class="feature-card"><h3>{title}</h3><p>{description}</p></div>',
            unsafe_allow_html=True,
        )

st.subheader("Perguntas frequentes")
with st.expander("A assistente substitui uma formação profissional?"):
    st.write(
        "Não. Ela ajuda com informações gerais, mas não substitui cursos, "
        "prática supervisionada, instruções dos fabricantes nem avaliação "
        "profissional presencial."
    )
with st.expander("Onde consulto os valores dos cursos?"):
    st.write(
        "Os preços, datas e vagas podem mudar. Confirma as condições atuais "
        "diretamente nos canais oficiais do Casal da Unha."
    )
with st.expander("A assistente pode orientar sobre saúde das unhas?"):
    st.write(
        "Pode explicar cuidados gerais, mas não diagnostica nem trata doenças. "
        "Em caso de dor, inflamação, descolamento ou alteração suspeita, "
        "interrompe o procedimento e procura um profissional de saúde."
    )

st.subheader("Legenda pronta para partilhar")
st.code(
    "💅 Já conhece a assistente virtual do Casal da Unha? "
    "Converse sobre técnicas de unhas, gel de construção, esmaltação, "
    "biossegurança e carreira nail designer. Uma ajudinha acolhedora para "
    "organizar ideias e valorizar o teu trabalho! ✨ "
    "Acesse pelo link e venha conversar. Respostas com IA sujeitas à "
    "disponibilidade do serviço.",
    language=None,
)
