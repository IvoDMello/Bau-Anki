# WordVault (Projeto Baú Anki) 📚

Um gerenciador de vocabulário gamificado, *local-first*, que evolui visualmente conforme o progresso do estudante. O projeto serve como um hub intermediário para coletar palavras antes de enviá-las para o Anki (SRS) via API.

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)

## 🎯 Objetivo do Projeto

Resolver a fricção de adicionar palavras diretamente no Anki, criando uma interface intermediária agradável que recompensa a consistência.
O sistema implementa uma lógica de **"Evolução de Interface"**: o app começa com um design rústico (Nível 0) e desbloqueia CSS moderno (Nível 1, 2) conforme o banco de dados de palavras cresce.

## 🛠️ Stack Tecnológico

* **Backend & Lógica:** Python 3.12, Flask.
* **Banco de Dados:** SQLite (Modelagem via SQLAlchemy ORM).
* **Frontend:** Jinja2, HTML5, CSS Dinâmico (injeção baseada em regras de negócio).
* **Integração:** REST API (Consumo da API local `anki-connect`).

## ⚙️ Funcionalidades

1.  **CRUD de Palavras:** Adição rápida de Termo, Significado e Exemplos.
2.  **Gamificação de Interface:**
    * *Nível 0 (< 5 palavras):* Estilo "Terminal/Raw HTML".
    * *Nível 1 (5+ palavras):* Estilo Clean (PicoCSS).
    * *Nível 2 (20+ palavras):* Estilo Premium (Dark Mode/Glassmorphism).
3.  **Analytics Simples:** Contadores de palavras totais e sessões diárias.
4.  **Sincronização:** Botão para empurrar (Push) cards formatados diretamente para o Anki Desktop.

## 🚀 Como Rodar Localmente

### Pré-requisitos
* Python 3.10+
* Anki Desktop (com o add-on AnkiConnect instalado) - *Opcional para rodar, necessário para sincronizar.*

### Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SEU_USUARIO/bau-anki.git](https://github.com/SEU_USUARIO/bau-anki.git)
    cd bau-anki
    ```

2.  **Configure o Ambiente Virtual (Boa Prática):**
    ```bash
    python -m venv .venv
    # Windows
    .\.venv\Scripts\Activate
    # Linux/Mac
    source .venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as Variáveis:**
    Crie um arquivo `.env` na raiz (use `.env.example` como base):
    ```ini
    FLASK_APP=app.py
    FLASK_ENV=development
    DATABASE_URL=sqlite:///bau.db
    SECRET_KEY=sua_chave_secreta_aqui
    ```

5.  **Execute:**
    ```bash
    python app.py
    ```
    Acesse em: `http://127.0.0.1:5000`

## 📂 Estrutura de Pastas

## 📝 Próximos Passos (Roadmap)

* [ ] Dashboard com gráficos de frequência de estudo (Plotly/Matplotlib).
* [ ] Pipeline de NLP para buscar definições automáticas.
* [ ] Exportação para CSV/Excel para análise de dados.

---
*Desenvolvido por Ivo como projeto de portfólio em Engenharia de Dados e Backend.*