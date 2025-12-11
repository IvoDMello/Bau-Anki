def calculate_level(total_words, unique_words):
    """
    Define o nível do usuário baseado no volume de dados.
    A lógica agora controla as imagens do Baú e do Fundo (Background).
    """
    
    # NÍVEL 1: O Início (0 a 4 palavras)
    if total_words < 5:
        return {
            "level": 1,
            "title": "Jovem Gafanhoto",
            "style_mode": "level-1",
            "chest_image": "css/BauNvl1.png", 
            "bg_image": "css/FundoNvl1.png",
            "next_goal": 5
        }
    
    # NÍVEL 2: Aprendiz (5 a 19 palavras)
    elif total_words < 20:
        return {
            "level": 2,
            "title": "Aprendiz de CSS",
            "style_mode": "level-2",
            "chest_image": "baunvl2.png",
            "bg_image": "fundonvl2.png",
            "next_goal": 20
        }
    
    # NÍVEL 3: Mestre (20 a 49 palavras)
    elif total_words < 50:
        return {
            "level": 3,
            "title": "Mestre do Design",
            "style_mode": "level-3",
            "chest_image": "baunvl3.png",
            "bg_image": "fundonvl3.png",
            "next_goal": 50
        }
        
    # NÍVEL 4: Lenda (50+ palavras)
    else:
        return {
            "level": 4,
            "title": "Lenda do Fullstack",
            "style_mode": "level-4",
            "chest_image": "baunvl4.png",
            "bg_image": "fundonvl4.png",
            "next_goal": None
        }