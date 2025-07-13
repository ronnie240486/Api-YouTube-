from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/buscar")
def buscar_produtos(termo: str):
    # Simulado com mais métricas
    return {
        "produtos": [
            {
                "nome": f"{termo.title()} Premium 2025",
                "preco": "R$ 279,99",
                "imagem": "https://via.placeholder.com/250",
                "avaliacoes": 1640,
                "estrelas": 4.8,
                "link": "https://www.amazon.com.br/produto-exemplo",
                "em_alta": True
            }
        ]
    }
