from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Entry(db.Model):
    __tablename__ = "entries"
    
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(200), nullable=False)
    meaning = db.Column(db.Text, nullable=True)
    example = db.Column(db.Text, nullable=True)
    
    # Metadados do Anki
    deck = db.Column(db.String(120), default="English::Inbox")
    model = db.Column(db.String(120), default="Basic")
    tags = db.Column(db.String(240), default="anki-bau")
    anki_note_id = db.Column(db.BigInteger, nullable=True)
    unique_key = db.Column(db.String(220), index=True)
    
    # --- NOVO: Campos para o Algoritmo SRS (Spaced Repetition) ---
    # Algoritmo base: SM-2 (SuperMemo 2)
    next_review = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    interval = db.Column(db.Integer, default=0)      # Dias até a próxima revisão
    ease_factor = db.Column(db.Float, default=2.5)   # Dificuldade (2.5 é o padrão inicial)
    repetitions = db.Column(db.Integer, default=0)   # Quantas vezes acertou consecutivamente
    review_count = db.Column(db.Integer, default=0)  # Total de revisões feitas
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)