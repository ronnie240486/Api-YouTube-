from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/buscar")
def buscar_amazon(termo: str = Query(...)):
    # Simulado com dados fictícios
    return {"produtos": [
        {
            "nome": f"Produto {termo} Premium",
            "preco": "R$ 199,90",
            "imagem": "https://via.placeholder.com/200",
            "link": "https://www.amazon.com.br"
        }
    ]}
