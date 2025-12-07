# services/gamification.py

def calculate_level(total_words, unique_words):
    """
    Define o nível do usuário baseado no volume de dados.
    Data Science thinking: Feature Engineering simples.
    """
    if total_words < 5:
        return {
            "level": 0,
            "title": "Novato do ASCII",
            "style_mode": "bare-bones", # Sem CSS, feio
            "next_goal": 5
        }
    elif total_words < 20:
        return {
            "level": 1,
            "title": "Aprendiz de CSS",
            "style_mode": "basic-css", # CSS Padrão (Pico)
            "next_goal": 20
        }
    else:
        return {
            "level": 2,
            "title": "Mestre do Design",
            "style_mode": "premium", # Seu CSS customizado bonito
            "next_goal": None
        }