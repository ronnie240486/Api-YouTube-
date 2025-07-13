
from fastapi import APIRouter, Query
import httpx
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

@router.get("/buscar")
async def buscar_videos(termo: str = Query(...)):
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={termo}&type=video&maxResults=5&key={YOUTUBE_API_KEY}"

    async with httpx.AsyncClient() as client:
        search_response = await client.get(search_url)
        search_data = search_response.json()

        video_ids = ",".join([item["id"]["videoId"] for item in search_data.get("items", [])])
        stats_url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics,contentDetails&id={video_ids}&key={YOUTUBE_API_KEY}"
        stats_response = await client.get(stats_url)
        stats_data = {item["id"]: item for item in stats_response.json().get("items", [])}

    videos = []
    for item in search_data.get("items", []):
        video_id = item["id"]["videoId"]
        stats = stats_data.get(video_id, {})
        snippet = item["snippet"]

        views = int(stats.get("statistics", {}).get("viewCount", 0))
        cpm = 15.00  # CPM simulado
        receita = (views / 1000) * cpm
        duration = stats.get("contentDetails", {}).get("duration", "N/A")

        videos.append({
            "videoId": video_id,
            "titulo": snippet["title"],
            "canal": snippet["channelTitle"],
            "thumbnail": snippet["thumbnails"]["medium"]["url"],
            "views": f"{views:,}",
            "cpm": f"R$ {cpm:.2f}",
            "receita": f"R$ {receita:.2f}",
            "duracao": duration
        })

    return {"videos": videos}
