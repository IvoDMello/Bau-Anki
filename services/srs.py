from datetime import datetime, timedelta

def calculate_next_review(quality, previous_interval, previous_ease):
    """
    Implementação do Algoritmo SM-2 (Anki).
    
    :param quality: Nota do usuário (0 a 5). 
                    0-2: Falha (Repetir hoje). 
                    3-5: Sucesso (Avançar).
    :param previous_interval: Dias desde a última revisão.
    :param previous_ease: Fator de facilidade atual (padrão 2.5).
    
    :return: (novo_intervalo, novo_ease, data_proxima_revisao)
    """
    
    # 1. Se a nota for menor que 3, consideramos que o usuário esqueceu.
    if quality < 3:
        new_interval = 1 # Reseta para 1 dia
        new_ease = previous_ease # Não penalizamos o Ease drasticamente no erro imediato
        next_date = datetime.utcnow() + timedelta(minutes=10) # Revisa em 10 min (simbólico)
        return new_interval, new_ease, next_date

    # 2. Calcular novo Fator de Facilidade (Ease Factor)
    # Fórmula mágica do SM-2: EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    new_ease = previous_ease + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    if new_ease < 1.3: # O limite mínimo do SM-2 é 1.3
        new_ease = 1.3

    # 3. Calcular novo Intervalo (em dias)
    if previous_interval == 0:
        new_interval = 1
    elif previous_interval == 1:
        new_interval = 6
    else:
        new_interval = int(previous_interval * new_ease)

    # 4. Calcular Data
    next_date = datetime.utcnow() + timedelta(days=new_interval)

    return new_interval, new_ease, next_date