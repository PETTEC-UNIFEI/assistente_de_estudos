import streamlit as st
from main import load_index_and_model, search_context, generate_answer

st.title("Assistente RAG Local com PDFs")

index, chunks, model = load_index_and_model()

pergunta = st.text_input("Digite sua pergunta:")

if pergunta:
    contexto = "\n\n".join(search_context(index, chunks, pergunta, model))
    resposta = generate_answer(contexto, pergunta)
    with st.expander("🔍 Ver trechos utilizados na resposta"):
        st.code(contexto)


    st.markdown("### Resposta:")
    st.write(resposta)
