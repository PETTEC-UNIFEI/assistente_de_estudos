# Assistente de Estudos — Bot RAG (Streamlit + Ollama)

Este projeto é um bot de estudo com **RAG** (Retrieval-Augmented Generation) e interface em **Streamlit**.

## Pré-requisitos
- **Python 3.10+** (recomendado 3.11)
- **Git**
- **Ollama** instalado (para usar o modelo local `mistral`)

---

## Passo a passo (Windows)

### 1) Clonar o repositório e entrar na pasta
```bat
git clone https://github.com/PETTEC-UNIFEI/assistente_de_estudos.git
cd assistente_de_estudos
```

### 2) Criar e ativar ambiente virtual
Crie o ambiente:
```bat
python -m venv venv
```

Ative **no Prompt de Comando (cmd.exe)**:
```bat
venv\Scripts\activate
```

> Se usar **PowerShell**, ative com:
```powershell
.env\Scripts\Activate.ps1
```

### 3) Instalar dependências
```bat
pip install --upgrade pip
pip install -r requirements.txt
```

### 4) Adicionar PDFs e construir o índice
Coloque seus arquivos **.pdf** dentro da pasta `pdfs/` e rode:
```bat
python build_index.py
```

### 5) Baixar o modelo do Ollama
```bat
ollama pull mistral
```

### 6) Rodar a interface
```bat
streamlit run app.py
```

---

## Observações rápidas
- Se aparecer erro ao instalar **faiss-cpu** no Windows, tente:
  ```bat
  pip install faiss-cpu==1.7.4
  ```
- Em muitos casos, o **Ollama** já roda como serviço no Windows; não é necessário usar `ollama serve` manualmente.
