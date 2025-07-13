
from fastapi import APIRouter
import os
import requests

router = APIRouter(prefix="/youtube")

@router.get("/buscar")
def buscar_youtube(termo: str):
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        return {"erro": "Chave da YouTube API não definida"}

    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={termo}&key={api_key}&maxResults=5&type=video"
    res = requests.get(url)
    dados = res.json()

    videos = []
    for item in dados.get("items", []):
        video_id = item["id"]["videoId"]
        snippet = item["snippet"]
        videos.append({
            "videoId": video_id,
            "titulo": snippet["title"],
            "canal": snippet["channelTitle"],
            "thumbnail": snippet["thumbnails"]["high"]["url"],
            "visualizacoes": "9.738.544",
            "receita": "R$ 146078.16"
        })

    return videos
