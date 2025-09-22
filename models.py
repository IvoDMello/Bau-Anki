from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Entry(db.Model):
    __tablename__ = "entries"
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(200), nullable=False)
    meaning = db.Column(db.Text, nullable=True)
    example = db.Column(db.Text, nullable=True)
    deck = db.Column(db.String(120), default="English::Inbox")
    model = db.Column(db.String(120), default="Basic")
    tags = db.Column(db.String(240), default="anki-bau")
    anki_note_id = db.Column(db.BigInteger, nullable=True)
    unique_key = db.Column(db.String(220), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
