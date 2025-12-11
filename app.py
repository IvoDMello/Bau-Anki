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

# --- Context Processor (Variáveis Globais) ---
@app.context_processor
def inject_globals():
    # Garante que 'total' esteja disponível em TODAS as telas (evita erros no base.html)
    return dict(total=S.count_total())

# --- ROTA: HOME / DASHBOARD ---
@app.get("/")
def index():
    # Analytics
    total = S.count_total()
    today = S.count_today()
    by_tag = S.count_by_tag()
    
    # Cards vencidos (Due)
    now = datetime.utcnow()
    due_count = Entry.query.filter(
        (Entry.next_review <= now) | (Entry.next_review == None)
    ).count()

    # Gamificação
    gamification = calculate_level(total, total)
    
    # Lista de últimas entradas para exibir na home (Opcional, mas útil)
    entries = Entry.query.order_by(Entry.created_at.desc()).limit(10).all()
    
    return render_template(
        "index.html", 
        entries=entries, 
        today=today, 
        by_tag=by_tag,
        gamification=gamification,
        due_count=due_count,
        total=total
    )

# --- ROTAS DE ESTUDO (SRS) ---
@app.get("/study")
def study_session():
    total = S.count_total()
    gamification = calculate_level(total, total)

    # Busca card pendente (Vencido ou Novo)
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
    
    # Atualiza no Banco
    card.interval = new_interval
    card.ease_factor = new_ease
    card.next_review = next_date
    card.review_count += 1
    
    if grade >= 3:
        card.repetitions += 1
    else:
        card.repetitions = 0
        
    db.session.commit()
    return redirect(url_for("study_session"))

# --- ROTA: ADICIONAR NOVA PALAVRA ---
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

# --- NOVAS ROTAS (Edição e Anki) ---

@app.route("/entry/<int:id>", methods=["GET"])
def detail(id):
    """Exibe a tela de detalhes/edição de uma palavra específica."""
    entry = Entry.query.get_or_404(id)
    
    # Necessário para manter o estilo visual correto
    total = S.count_total()
    gamification = calculate_level(total, total)
    
    return render_template("detail.html", e=entry, gamification=gamification)

@app.post("/entry/<int:id>/edit")
def edit_entry(id):
    """Processa o formulário de edição."""
    entry = Entry.query.get_or_404(id)
    
    # Atualiza os campos com o que veio do form
    entry.term = request.form.get("term")
    entry.meaning = request.form.get("meaning")
    entry.example = request.form.get("example")
    entry.deck = request.form.get("deck")
    entry.model = request.form.get("model")
    entry.tags = request.form.get("tags")
    
    # Tenta atualizar no Anki se já estiver sincronizado
    if entry.anki_note_id:
        try:
            fields = {
                "Front": entry.term,
                "Back": entry.meaning
            }
            # Se quiser enviar o exemplo junto, concatenamos no Back (opcional)
            if entry.example:
                fields["Back"] += f"<br><br><small>{entry.example}</small>"

            update_note_fields(entry.anki_note_id, fields)
            flash("Atualizado no Baú e no Anki!", "success")
        except Exception as e:
            # Não impede de salvar no banco local, apenas avisa
            flash(f"Salvo no Baú, mas erro no Anki: {e}", "warning")
    else:
        flash("Entrada atualizada.", "success")
        
    db.session.commit()
    return redirect(url_for("detail", id=id))

@app.post("/push/<int:id>")
def push_to_anki(id):
    """Envia uma nota nova para o Anki via AnkiConnect."""
    entry = Entry.query.get_or_404(id)
    
    if entry.anki_note_id:
        flash("Essa nota já parece estar no Anki (ID existe).", "info")
        return redirect(url_for("detail", id=id))
        
    try:
        # Prepara os campos
        fields = {
            "Front": entry.term,
            "Back": entry.meaning or ""
        }
        if entry.example:
            fields["Back"] += f"<br><br><small>{entry.example}</small>"

        # Prepara tags
        tags = entry.tags.split() if entry.tags else ["wordvault"]
        
        # Chama a API (ankiconnect.py)
        note_id = add_note(
            deck=entry.deck,
            model=entry.model,
            fields=fields,
            tags=tags,
            allow_duplicate=False
        )
        
        # Salva o ID retornado
        entry.anki_note_id = note_id
        db.session.commit()
        
        flash(f"Sucesso! Nota criada no Anki (ID: {note_id})", "success")
        
    except Exception as e:
        flash(f"Erro ao conectar com Anki: {str(e)}", "error")
        
    return redirect(url_for("detail", id=id))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)