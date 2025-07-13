
from fastapi import APIRouter, Query
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

@router.get("/buscar")
async def buscar_videos(termo: str = Query(...), max_results: int = 5):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": termo,
        "type": "video",
        "maxResults": max_results,
        "key": YOUTUBE_API_KEY
    }

    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params)
        dados = r.json()

    videos = []
    for item in dados.get("items", []):
        video_id = item["id"]["videoId"]
        snippet = item["snippet"]
        titulo = snippet["title"]
        canal = snippet["channelTitle"]
        thumb = snippet["thumbnails"]["high"]["url"]
        publicado = snippet["publishedAt"]

        cpm = 15.0
        views = 100000
        receita = round((views / 1000) * cpm, 2)

        videos.append({
            "videoId": video_id,
            "titulo": titulo,
            "canal": canal,
            "thumbnail": thumb,
            "publicado": publicado,
            "views": views,
            "cpm": f"R$ {cpm:.2f}",
            "receita": f"R$ {receita:.2f}",
            "hashtags": ["#viral", "#destaque", "#tendência"]
        })

    return {"videos": videos}
