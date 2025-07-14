from fastapi import APIRouter, Query
from utils.youtube_api import buscar_videos

router = APIRouter()

@router.get("/youtube/buscar")
def buscar_youtube(termo: str = Query(...), pais: str = Query(default="BR")):
    return buscar_videos(termo, pais)
