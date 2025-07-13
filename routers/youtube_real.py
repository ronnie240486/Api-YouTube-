
from fastapi import APIRouter, Query
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

@router.get("/buscar")
async def buscar_videos(termo: str = Query(...)):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={termo}&type=video&maxResults=5&key={YOUTUBE_API_KEY}"

    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        data = res.json()

    videos = []
    for item in data.get("items", []):
        video_id = item["id"]["videoId"]
        titulo = item["snippet"]["title"]
        canal = item["snippet"]["channelTitle"]
        thumbnail = item["snippet"]["thumbnails"]["medium"]["url"]
        views = "Simulado"
        cpm = "R$ 15,00"
        receita = "R$ 100,00"

        videos.append({
            "videoId": video_id,
            "titulo": titulo,
            "canal": canal,
            "thumbnail": thumbnail,
            "views": views,
            "cpm": cpm,
            "receita": receita
        })

    return {"videos": videos}
