from fastapi import APIRouter, Query
from typing import List
from datetime import datetime, timezone
import requests

router = APIRouter()

API_KEY = "SUA_CHAVE_YOUTUBE_API"
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"
VIDEOS_API_URL = "https://www.googleapis.com/youtube/v3/videos"

def calcular_cpm(views):
    if views < 1000:
        return "R$ 0,00"
    elif views < 5000:
        return "R$ 5,00"
    elif views < 10000:
        return "R$ 8,00"
    else:
        return "R$ 15,00"

@router.get("/youtube/viralizar")
def buscar_videos_virais(termo: str = Query(..., min_length=2)):
    params = {
        "part": "snippet",
        "q": termo,
        "type": "video",
        "order": "date",
        "maxResults": 5,
        "key": API_KEY
    }
    r = requests.get(YOUTUBE_API_URL, params=params)
    resultados = r.json()

    video_ids = [item["id"]["videoId"] for item in resultados.get("items", [])]

    detalhes_params = {
        "part": "statistics,snippet,contentDetails",
        "id": ",".join(video_ids),
        "key": API_KEY
    }
    detalhes_res = requests.get(VIDEOS_API_URL, params=detalhes_params)
    detalhes = detalhes_res.json()

    videos = []
    for item in detalhes.get("items", []):
        snippet = item["snippet"]
        stats = item["statistics"]
        publicado_em = snippet["publishedAt"]
        data_publicacao = datetime.fromisoformat(publicado_em.replace("Z", "+00:00"))
        agora = datetime.now(timezone.utc)
        horas = (agora - data_publicacao).total_seconds() / 3600
        views = int(stats.get("viewCount", 0))
        views_por_hora = views / horas if horas > 0 else views

        videos.append({
            "titulo": snippet["title"],
            "canal": snippet["channelTitle"],
            "thumbnail": snippet["thumbnails"]["high"]["url"],
            "link": f"https://www.youtube.com/watch?v={item['id']}",
            "views": views,
            "publicado_em": data_publicacao.strftime("%d/%m/%Y %H:%M"),
            "duracao": item["contentDetails"]["duration"],
            "cpm_estimado": calcular_cpm(views),
            "views_por_hora": round(views_por_hora, 2)
        })

    videos.sort(key=lambda x: x["views_por_hora"], reverse=True)
    return videos