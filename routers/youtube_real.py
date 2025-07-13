import requests
from fastapi import APIRouter, Query
from datetime import datetime
import os

router = APIRouter()

YOUTUBE_API_KEY = "AIzaSyAU4tiYbFlS3Gn68OmsmRqJQnbGKWVpJxQ"
SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
VIDEO_DETAILS_URL = "https://www.googleapis.com/youtube/v3/videos"

@router.get("/buscar")
def buscar_videos(termo: str, pais: str = "BR", max_results: int = 5):
    params_search = {
        "part": "snippet",
        "q": termo,
        "regionCode": pais,
        "type": "video",
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY
    }

    search_response = requests.get(SEARCH_URL, params=params_search).json()

    if "items" not in search_response:
        return {"erro": "Erro ao buscar vídeos no YouTube"}

    video_ids = [item["id"]["videoId"] for item in search_response["items"]]
    if not video_ids:
        return {"erro": "Nenhum vídeo encontrado"}

    params_details = {
        "part": "statistics,snippet,contentDetails",
        "id": ",".join(video_ids),
        "key": YOUTUBE_API_KEY
    }

    details_response = requests.get(VIDEO_DETAILS_URL, params=params_details).json()
    resultados = []

    for item in details_response.get("items", []):
        stats = item.get("statistics", {})
        snippet = item.get("snippet", {})
        details = item.get("contentDetails", {})

        view_count = int(stats.get("viewCount", 0))
        duration = details.get("duration", "PT0M")
        published_at = snippet.get("publishedAt", "")
        title = snippet.get("title", "Sem título")
        channel = snippet.get("channelTitle", "")
        thumbnails = snippet.get("thumbnails", {})
        image = thumbnails.get("medium", {}).get("url", "")
        video_id = item["id"]

        receita = round((view_count / 1000) * 15.0, 2)
        tempo = "Data: " + published_at[:10]

        resultados.append({
            "titulo": title,
            "visualizacoes": view_count,
            "receita_estimada": receita,
            "duracao": duration,
            "tempo": tempo,
            "canal": channel,
            "inscritos": 0,
            "hashtags": [],
            "cpm": 15.00,
            "imagem": image,
            "link": f"https://www.youtube.com/watch?v={video_id}",
            "em_alta": view_count > 1000000
        })

    return {"videos": resultados}
