# WordVault (Baú de Palavras) — MVP

App local (Flask + SQLite) que integra com **Anki** via **AnkiConnect**, para cadastrar termos, enviar/atualizar notas e visualizar contadores. Base para gamificação e onboarding de SRS.

## Requisitos
- Python 3.10+
- Anki instalado
- Add-on **AnkiConnect** (ID: 2055492159) — abra o Anki, instale o addon e mantenha o Anki aberto enquanto usa o app.

## Como rodar
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
# source .venv/bin/activate

pip install -r requirements.txt

# copie .env.example para .env e ajuste se quiser
# Windows (PowerShell):
Copy-Item .env.example .env
# Linux/macOS:
# cp .env.example .env

python app.py
```
Abra http://127.0.0.1:5000 (deixe o Anki aberto).

## Estrutura
```
cofre-anki/
├─ app.py
├─ ankiconnect.py
├─ models.py
├─ services/
│   ├─ normalizer.py
│   └─ stats.py
├─ templates/
│   ├─ base.html
│   ├─ index.html
│   └─ detail.html
├─ static/
│   └─ themes/
├─ scripts/
│   └─ test_anki.py
├─ requirements.txt
└─ .env.example
```

## Próximos passos
- Gamificação: achievements, temas/skins.
- Leitura de reviews (interval/accuracy) para “aprendida v2”.
- PWA/Mobile, onboarding (curso de 7 dias).

## Usando MySQL
1) Instale o servidor MySQL e crie o banco/usuário (exemplo):
```sql
CREATE DATABASE wordvault CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'usuario'@'localhost' IDENTIFIED BY 'senha';
GRANT ALL PRIVILEGES ON wordvault.* TO 'usuario'@'localhost';
FLUSH PRIVILEGES;
```

2) No arquivo `.env` defina:
```
DATABASE_URL=mysql+pymysql://usuario:senha@localhost:3306/wordvault
```

3) Instale as dependências (inclui PyMySQL) e rode:
```bash
pip install -r requirements.txt
python app.py
```
