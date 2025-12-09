from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Entry(db.Model):
    __tablename__ = "entries"
    
    id = db.Column(db.Integer, primary_key=True)
    
    # --- CONTEÚDO ---
    target_word = db.Column(db.String(100), nullable=True) # A palavra do dia (ex: "staring")
    term = db.Column(db.Text, nullable=False)              # A FRASE completa (Front)
    meaning = db.Column(db.Text, nullable=True)            # A tradução/definição (Back)
    example = db.Column(db.Text, nullable=True)            # Notas extras
    
    # --- FLUXO DE TRABALHO ---
    # 'inbox' = Capturado na rua, precisa gerar frase
    # 'active' = Frase pronta, pode estudar
    status = db.Column(db.String(20), default="active") 
    
    # --- METADADOS ANKI ---
    deck = db.Column(db.String(120), default="English::Inbox")
    model = db.Column(db.String(120), default="Basic")
    tags = db.Column(db.String(240), default="anki-bau")
    anki_note_id = db.Column(db.BigInteger, nullable=True)
    unique_key = db.Column(db.String(220), index=True)
    
    # --- ALGORITMO SRS (SM-2) ---
    next_review = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    interval = db.Column(db.Integer, default=0)
    ease_factor = db.Column(db.Float, default=2.5)
    repetitions = db.Column(db.Integer, default=0)
    
    review_count = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)