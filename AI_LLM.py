import requests
import os
import os
from dotenv import load_dotenv
import requests

load_dotenv()  # chama aqui também para garantir

API_KEY = os.getenv("DEEPSEEK_API_KEY")

def resposta_deepseek(pergunta):
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Você é o assistente oficial da empresa Lumora Sync. "
                            "Responda de forma clara, profissional e tecnológica."
                        )
                    },
                    {"role": "user", "content": pergunta}
                ],
                "temperature": 0.7
            }
        )

        data = response.json()
        
        # DEBUG: Mostra retorno em caso de erro
        if "choices" not in data:
            print("🧩 RESPOSTA DA API:", data)  # Mostra o conteúdo retornado
            return f"Erro: resposta inesperada da API. Detalhes: {data.get('error', 'sem detalhes')}"
        
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Erro ao acessar o LLM: {e}"
