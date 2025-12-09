# seed_data.py
from app import app, db
from models import Entry
from datetime import datetime

# Sua lista curada (Target Word | Frase Completa | Significado/Contexto)
data = [
    {
        "target": "onwards",
        "phrase": "We need to move onwards, not backwards.",
        "meaning": "Adiante / Em frente"
    },
    {
        "target": "creeping",
        "phrase": "Sunlight comes creeping in, Illuminates our skin.",
        "meaning": "Entrando sorrateiramente / devagar (Letra de música)"
    },
    {
        "target": "thought",
        "phrase": "Just from the thought of you.",
        "meaning": "Só de pensar em você"
    },
    {
        "target": "staring",
        "phrase": "It is rude to keep staring at strangers.",
        "meaning": "Olhando fixamente / Encarando"
    },
    {
        "target": "sink",
        "phrase": "Put the dirty dishes in the sink.",
        "meaning": "Pia (de cozinha)"
    },
    {
        "target": "veneer",
        "phrase": "The table has a nice oak veneer, but it's cheap wood inside.",
        "meaning": "Revestimento / Lâmina de madeira (Aparência externa)"
    },
    {
        "target": "wreck",
        "phrase": "Don't let your anger wreck it all.",
        "meaning": "Estragar tudo / Destruir"
    },
    {
        "target": "owning",
        "phrase": "And you'll be owning all the fines.",
        "meaning": "Arcando / Assumindo (as multas)"
    },
    {
        "target": "bruised",
        "phrase": "I fell off my bike and bruised my knee.",
        "meaning": "Machucou / Fez um hematoma"
    },
    {
        "target": "smoke",
        "phrase": "My plans went up in smoke.",
        "meaning": "Foram por água abaixo (Expressão)"
    },
    {
        "target": "charts",
        "phrase": "The song is number one on the music charts.",
        "meaning": "Paradas (de sucesso) / Gráficos"
    },
    {
        "target": "loan",
        "phrase": "I took out a loan to buy my house.",
        "meaning": "Empréstimo"
    },
    {
        "target": "claim",
        "phrase": "He made a false claim about the accident.",
        "meaning": "Afirmação / Reivindicação"
    },
    {
        "target": "toss and turn",
        "phrase": "I usually toss and turn afterwards.",
        "meaning": "Me reviro (na cama/sono)"
    },
    {
        "target": "unbidden",
        "phrase": "Strange thoughts came unbidden into your head.",
        "meaning": "Sem serem chamados / Espontaneamente"
    },
    {
        "target": "padiding",
        "phrase": "It was all padiding.",
        "meaning": "[Revisar ortografia] Possivelmente 'parading' ou gíria específica."
    },
    {
        "target": "aggrieved",
        "phrase": "The aggrieved customer asked for a refund.",
        "meaning": "Lesado / Ofendido / Prejudicado"
    }
]

def seed():
    with app.app_context():
        print("🌱 Iniciando o plantio de dados...")
        
        # Opcional: Limpar dados antigos para não duplicar se rodar 2x
        # Entry.query.delete()
        
        count = 0
        for item in data:
            # Verifica se já existe para não duplicar
            exists = Entry.query.filter_by(term=item["phrase"]).first()
            if not exists:
                entry = Entry(
                    target_word=item["target"],
                    term=item["phrase"],     # A Frase vai no campo 'term' (Front)
                    meaning=item["meaning"], # A Tradução vai no 'meaning' (Back)
                    status="active",         # Já nasce pronto para estudar
                    created_at=datetime.utcnow()
                )
                db.session.add(entry)
                count += 1
        
        db.session.commit()
        print(f"✅ {count} novas frases inseridas no Baú!")

if __name__ == "__main__":
    seed()