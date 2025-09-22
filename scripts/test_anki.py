"""Teste rápido da integração com AnkiConnect.
Execute com o Anki aberto e o add-on AnkiConnect instalado.
"""
import os, sys, time
from ankiconnect import version, create_deck, add_note, update_note_fields, find_notes, notes_info

DECK = os.getenv("DEFAULT_DECK", "English::Inbox")
MODEL = os.getenv("DEFAULT_MODEL", "Basic")

def main():
    print("AnkiConnect version:", version())
    print("Garantindo deck:", DECK)
    create_deck(DECK)

    print("Adicionando nota de teste...")
    nid = add_note(DECK, MODEL, {"Front": "hello", "Back": "olá"}, tags=["test", "wordvault"])
    print("Note id:", nid)

    print("Procurando a nota...")
    ids = find_notes(f'deck:"{DECK}" hello')
    print("Encontradas:", ids)

    print("Atualizando a nota...")
    update_note_fields(nid, {"Front": "hello", "Back": "olá — atualizado"})
    info = notes_info([nid])[0]
    print("Campos atuais:", info.get("fields", {}))

    print("OK. Integração básica funcionando.")

if __name__ == "__main__":
    main()
