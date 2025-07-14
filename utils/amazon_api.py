import os

def buscar_produtos_amazon(termo):
    access = os.getenv("AMAZON_ACCESS_KEY")
    secret = os.getenv("AMAZON_SECRET_KEY")
    tag = os.getenv("AMAZON_TAG")
    region = os.getenv("AMAZON_REGION")

    if not access or not secret or not tag:
        return {"erro": "Credenciais da Amazon não estão definidas no .env"}

    # Simulação de retorno real
    return {
        "produtos": [
            {
                "titulo": f"Produto exemplo para '{termo}'",
                "preco": "R$ 99,90",
                "imagem": "https://via.placeholder.com/150",
                "link": "https://www.amazon.com.br/"
            }
        ]
    }
