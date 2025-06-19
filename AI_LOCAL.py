def resposta_simples(pergunta):
    pergunta = pergunta.lower()

    if "oi" in pergunta:
        return "Oi! Eu sou o bot da Lumora Sync 💡"
    elif "quem é você" in pergunta:
        return "Sou um bot simples criado para a Lumora Sync, com IA embutida!"
    elif "horas" in pergunta:
        from datetime import datetime
        return f"Agora são {datetime.now().strftime('%H:%M')} ⏰"
    else:
        return "Desculpe, não entendi sua pergunta. Tente outra!"
