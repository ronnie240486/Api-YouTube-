from fastapi import APIRouter, Query

router = APIRouter()

@router.get("/buscar")
def buscar_videos(termo: str, pais: str = "BR"):
    # Simulação de dados com país e mais métricas
    return {
        "videos": [
            {
                "titulo": f"{termo.title()} Viral",
                "visualizacoes": 2480000,
                "receita_estimada": 745.35,
                "duracao": "PT4M10S",
                "tempo": "há 3 dias",
                "canal": "Canal Exemplo",
                "inscritos": 540000,
                "hashtags": ["#viral", "#trend", f"#{termo}"],
                "cpm": 16.90,
                "imagem": "https://i.ytimg.com/vi/xyz123/default.jpg",
                "link": "https://youtube.com/watch?v=xyz123",
                "em_alta": True
            }
        ]
    }
