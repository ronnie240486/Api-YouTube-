from fastapi import APIRouter, Query
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

@router.get("/buscar")
def buscar_videos(termo: str = Query(..., description="Termo de busca no YouTube")):
    try:
        resultados = youtube.search().list(
            q=termo,
            part="snippet",
            type="video",
            maxResults=6
        ).execute()

        videos = []
        for item in resultados["items"]:
            video_id = item["id"]["videoId"]
            snippet = item["snippet"]
            titulo = snippet["title"]
            canal = snippet["channelTitle"]
            thumbnail = snippet["thumbnails"]["high"]["url"]
            link = f"https://www.youtube.com/watch?v={video_id}"

            stats = youtube.videos().list(
                part="statistics,contentDetails",
                id=video_id
            ).execute()

            view_count = int(stats["items"][0]["statistics"].get("viewCount", 0))
            cpm = 15.00
            receita = round((view_count / 1000) * cpm, 2)

            videos.append({
                "titulo": titulo,
                "canal": canal,
                "views": view_count,
                "receita_estimada": f"R$ {receita:.2f}",
                "link": link,
                "thumbnail": thumbnail
            })

        return videos

    except Exception as e:
        return {"erro": str(e)}