import os, glob
import streamlit as st
from main import load_index_and_model, search_context, generate_answer

st.set_page_config(page_title="Assistente de Estudos RAG", layout="wide")

# ==== Estilos (CSS leve) ====
st.markdown("""
<style>
/* Hero com gradiente */
.hero {
  background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
  color: #fff;
  padding: 1.1rem 1.25rem;
  border-radius: 16px;
  margin-bottom: 1rem;
}
.hero h1 { margin: 0; font-size: 1.4rem; font-weight: 700; color: #ffffff; }
.hero p  { margin: .35rem 0 0 0; opacity: .92; }

/* Tabs com fonte mais forte */
.stTabs [data-baseweb="tab-list"] button { font-weight: 600; }

/* Bolha da resposta */
.answer-bubble {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 1rem;
}

/* Expander “cardificado” */
.st-expander > details {
  border: 1px solid #e2e8f0 !important;
  border-radius: 12px;
}
.st-expander > details > summary {
  font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ==== Header/Hero ====
st.markdown("""
<div class="hero">
  <h1>Assistente de Estudos RAG</h1>
  <p>Pesquise nos seus PDFs, obtenha respostas fundamentadas e veja as fontes.</p>
</div>
""", unsafe_allow_html=True)

# ==== Cache de recursos ====
@st.cache_resource(show_spinner=False)
def get_index_chunks_model():
    return load_index_and_model()

index, chunks, model = get_index_chunks_model()

# ==== Métricas rápidas ====
colA, colB, colC = st.columns(3)
pdf_count = len(glob.glob(os.path.join("pdfs", "*.pdf")))
chunk_count = len(chunks) if isinstance(chunks, list) else 0
# nome do modelo (fallbacks simples)
model_name = None
if isinstance(model, dict):
    model_name = model.get("model") or model.get("name") or model.get("model_name")
if not model_name:
    model_name = (str(model) or "desconhecido")[:32]

with colA:
    st.metric("PDFs indexados", pdf_count)
with colB:
    st.metric("Chunks", chunk_count)
with colC:
    st.metric("Modelo", model_name)

st.divider()

# ==== Estado compartilhado ====
if "last_question" not in st.session_state:
    st.session_state.last_question = None
if "last_answer" not in st.session_state:
    st.session_state.last_answer = None
if "last_sources" not in st.session_state:
    st.session_state.last_sources = []

# ==== Abas ====
tab_ask, tab_sources = st.tabs(["Perguntar", "Fontes"])

with tab_ask:
    st.subheader("Faça sua pergunta")
    question = st.text_input("Digite sua pergunta sobre os PDFs:", key="question_input")

    # Linha de controles mínimos
    col1, col2, col3 = st.columns([1, 1, 6])
    with col1:
        submit = st.button("Responder")
    with col2:
        clear = st.button("Limpar")

    if clear:
        for k in ("last_question", "last_answer", "last_sources", "question_input"):
            st.session_state.pop(k, None)
        st.rerun()

    if submit and question.strip():
        with st.spinner("Buscando trechos relevantes..."):
            # Mantém assinatura existente do seu backend
            ctx_list = search_context(index, chunks, question, model)
            contexto = "\n\n".join(ctx_list)

        with st.spinner("Gerando resposta..."):
            answer = generate_answer(contexto, question)

        st.session_state.last_question = question
        st.session_state.last_answer = answer
        st.session_state.last_sources = ctx_list

    # Exibição da resposta como “bolha”
    if st.session_state.last_answer:
        st.markdown("### Resposta")
        st.markdown(f"<div class='answer-bubble'>{st.session_state.last_answer}</div>", unsafe_allow_html=True)

with tab_sources:
    st.subheader("Fontes utilizadas na última resposta")
    if not st.session_state.last_sources:
        st.info("Ainda não há fontes para mostrar. Faça uma pergunta na aba **Perguntar**.")
    else:
        for i, chunk_text in enumerate(st.session_state.last_sources, start=1):
            with st.expander(f"Trecho {i}"):
                st.write(chunk_text)
