import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime

# Seus modelos e serviços
from models import db, Entry
from services.normalizer import to_unique_key
from services import stats as S
from services.gamification import calculate_level 
from services.srs import calculate_next_review    
from ankiconnect import create_deck, add_note, update_note_fields

load_dotenv()

DEFAULT_DECK = os.getenv("DEFAULT_DECK", "English::Inbox")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "Basic")
DEFAULT_TAGS = os.getenv("DEFAULT_TAGS", "anki-bau")

app = Flask(__name__)
# Configuração para MySQL (Docker) ou SQLite (Fallback)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///bau.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.getenv("FLASK_SECRET", "dev")

db.init_app(app)

# Cria o banco ao iniciar (se não existir)
with app.app_context():
    db.create_all()

# --- NOVO: Context Processor para injetar variáveis globais ---
@app.context_processor
def inject_globals():
    # Isso garante que 'total' esteja disponível em TODAS as telas (evita erros no base.html)
    return dict(total=S.count_total())

@app.get("/")
def index():
    # Analytics
    total = S.count_total() # (Ainda calculamos aqui para usar na gamificação)
    today = S.count_today()
    by_tag = S.count_by_tag()
    
    # --- A CORREÇÃO DO ERRO ESTÁ AQUI 👇 ---
    # Contar quantos cards vencem hoje ou antes (para o badge vermelho)
    now = datetime.utcnow()
    due_count = Entry.query.filter(
        (Entry.next_review <= now) | (Entry.next_review == None)
    ).count()
    # --------------------------------------

    # Gamificação
    gamification = calculate_level(total, total)
    
    # Busca as últimas entradas para a lista (opcional, se quiser mostrar abaixo)
    entries = Entry.query.order_by(Entry.created_at.desc()).limit(10).all()
    
    return render_template(
        "index.html", 
        entries=entries, 
        today=today, 
        by_tag=by_tag,
        gamification=gamification,
        due_count=due_count, # <--- Enviando a variável que faltava!
        total=total
    )

@app.get("/study")
def study_session():
    # Gamificação na tela de estudo
    total = S.count_total()
    gamification = calculate_level(total, total)

    # Busca card pendente
    now = datetime.utcnow()
    card = Entry.query.filter(
        (Entry.next_review <= now) | (Entry.next_review == None)
    ).order_by(Entry.next_review.asc()).first()

    if not card:
        return render_template("study_finished.html", gamification=gamification)

    return render_template("study_card.html", card=card, gamification=gamification)

@app.post("/study/<int:id>/grade")
def study_grade(id):
    card = Entry.query.get_or_404(id)
    grade = int(request.form.get("grade", 0))
    
    # Algoritmo SM-2
    new_interval, new_ease, next_date = calculate_next_review(
        grade, card.interval, card.ease_factor
    )
    
    # Atualiza
    card.interval = new_interval
    card.ease_factor = new_ease
    card.next_review = next_date
    card.review_count += 1 # Agora a coluna existe no banco!
    
    if grade >= 3:
        card.repetitions += 1
    else:
        card.repetitions = 0
        
    db.session.commit()
    return redirect(url_for("study_session"))

@app.post("/add")
def add():
    term = request.form["term"].strip()
    meaning = request.form.get("meaning","").strip()
    target_word = request.form.get("target_word", "").strip()
    
    # Defaults
    deck = DEFAULT_DECK
    model = DEFAULT_MODEL
    
    if not term:
        flash("A frase é obrigatória!")
        return redirect(url_for("index"))

    e = Entry(
        term=term, 
        meaning=meaning, 
        target_word=target_word,
        deck=deck, 
        model=model, 
        status="active",
        unique_key=to_unique_key(term)
    )
    db.session.add(e)
    db.session.commit()
    flash("Adicionado ao baú.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)