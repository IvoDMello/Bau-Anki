import os
import requests
from dotenv import load_dotenv

load_dotenv()
ANKI_URL = os.getenv("ANKI_URL", "http://127.0.0.1:8765")

class AnkiError(RuntimeError):
    pass

def _call(action, params=None, version=6, timeout=10):
    payload = {"action": action, "version": version}
    if params is not None:
        payload["params"] = params
    r = requests.post(ANKI_URL, json=payload, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    if data.get("error"):
        raise AnkiError(str(data["error"]))
    return data.get("result")

def version():
    return _call("version")

def create_deck(deck: str):
    return _call("createDeck", {"deck": deck})

def add_note(deck: str, model: str, fields: dict, tags=None, allow_duplicate=False):
    note = {
        "deckName": deck,
        "modelName": model,
        "fields": fields,
        "options": {
            "allowDuplicate": bool(allow_duplicate),
            "duplicateScope": "deck",
        },
        "tags": tags or [],
    }
    return _call("addNote", {"note": note})

def update_note_fields(note_id: int, fields: dict):
    return _call("updateNoteFields", {"note": {"id": int(note_id), "fields": fields}})

def find_notes(query: str):
    return _call("findNotes", {"query": query})

def notes_info(note_ids):
    return _call("notesInfo", {"notes": note_ids})
