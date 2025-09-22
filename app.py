import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from models import db, Entry
from services.normalizer import to_unique_key
from services import stats as S
from ankiconnect import create_deck, add_note, update_note_fields

load_dotenv()

DEFAULT_DECK = os.getenv("DEFAULT_DECK", "English::Inbox")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "Basic")
DEFAULT_TAGS = os.getenv("DEFAULT_TAGS", "anki-bau")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///bau.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.getenv("FLASK_SECRET", "dev")

db.init_app(app)

@app.before_first_request
def init_db():
    db.create_all()

@app.get("/")
def index():
    total = S.count_total()
    today = S.count_today()
    by_tag = S.count_by_tag()
    entries = Entry.query.order_by(Entry.created_at.desc()).limit(100).all()
    return render_template("index.html", entries=entries, total=total, today=today, by_tag=by_tag)

@app.post("/add")
def add():
    term = request.form["term"].strip()
    meaning = request.form.get("meaning","").strip()
    example = request.form.get("example","").strip()
    deck = request.form.get("deck", DEFAULT_DECK).strip() or DEFAULT_DECK
    model = request.form.get("model", DEFAULT_MODEL).strip() or DEFAULT_MODEL
    tags = request.form.get("tags", DEFAULT_TAGS).strip() or DEFAULT_TAGS

    e = Entry(term=term, meaning=meaning, example=example, deck=deck, model=model, tags=tags, unique_key=to_unique_key(term))
    db.session.add(e)
    db.session.commit()
    flash("Adicionado ao baú.")
    return redirect(url_for("index"))

@app.post("/push/<int:eid>")
def push(eid):
    e = Entry.query.get_or_404(eid)
    # criar deck se não existir
    create_deck(e.deck)
    fields = {"Front": e.term, "Back": f"{e.meaning}\n\n{e.example}".strip()}
    tags = [t.strip() for t in (e.tags or "").split() if t.strip()]
    if e.anki_note_id:
        update_note_fields(e.anki_note_id, fields)
        flash(f"Nota {e.anki_note_id} atualizada no Anki.")
    else:
        note_id = add_note(e.deck, e.model, fields, tags)
        e.anki_note_id = note_id
        db.session.commit()
        flash(f"Enviado ao Anki (note_id {note_id}).")
    return redirect(url_for("index"))

@app.get("/entry/<int:eid>")
def detail(eid):
    e = Entry.query.get_or_404(eid)
    return render_template("detail.html", e=e)

@app.post("/entry/<int:eid>/edit")
def edit(eid):
    e = Entry.query.get_or_404(eid)
    for field in ["term","meaning","example","deck","model","tags"]:
        val = request.form.get(field, getattr(e, field))
        setattr(e, field, val)
    e.unique_key = to_unique_key(e.term)
    db.session.commit()
    flash("Atualizado.")
    return redirect(url_for("detail", eid=e.id))

if __name__ == "__main__":
    app.run(debug=True)
