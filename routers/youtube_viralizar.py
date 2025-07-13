from fastapi import APIRouter, Query
import os
import requests
from datetime import datetime, timedelta
from dateutil import parser

router = APIRouter()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def format_duration(iso_duration):
    try:
        if "H" in iso_duration or "M" in iso_duration or "S" in iso_duration:
            duration = iso_duration.replace("PT", "")
            h, m, s = 0, 0, 0
            if "H" in duration:
                h = int(duration.split("H")[0])
                duration = duration.split("H")[1]
            if "M" in duration:
                m = int(duration.split("M")[0])
                duration = duration.split("M")[1]
            if "S" in duration:
                s = int(duration.replace("S", ""))
            return f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
    except:
        return "Desconhecida"

def tempo_publicacao(published_at):
    try:
        publicado = parser.isoparse(published_at)
        agora = datetime.utcnow()
        diff = agora - publicado
        dias = diff.days
        horas = diff.seconds // 3600
        if dias > 0:
            return f"{dias} dias"
        elif horas > 0:
            return f"{horas} horas"
        else:
            return "menos de 1 hora"
    except:
        return "Desconhecido"

@router.get("/viralizar")
def buscar_videos(termo: str = Query(...)):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={termo}&type=video&maxResults=10&key={YOUTUBE_API_KEY}"
    search_res = requests.get(url).json()

    resultados = []

    for item in search_res.get("items", []):
        video_id = item["id"]["videoId"]
        snippet = item["snippet"]
        titulo = snippet["title"]
        canal = snippet["channelTitle"]
        publicado_em = snippet["publishedAt"]
        thumbnail = snippet["thumbnails"]["high"]["url"]
        canal_id = snippet["channelId"]

        stats_url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics,contentDetails&id={video_id}&key={YOUTUBE_API_KEY}"
        stats_res = requests.get(stats_url).json()
        stats = stats_res.get("items", [{}])[0]

        views = int(stats.get("statistics", {}).get("viewCount", 0))
        likes = int(stats.get("statistics", {}).get("likeCount", 0))
        comentarios = int(stats.get("statistics", {}).get("commentCount", 0))
        engajamento = round((likes + comentarios) / views * 100, 2) if views else 0

        cpm = 15.0  # simulação
        receita = round((views / 1000) * cpm, 2)
        duracao = format_duration(stats.get("contentDetails", {}).get("duration", "PT0S"))
        tempo = tempo_publicacao(publicado_em)

        resultados.append({
            "titulo": titulo,
            "canal": canal,
            "canal_link": f"https://www.youtube.com/channel/{canal_id}",
            "canal_icone": f"https://yt3.ggpht.com/ytc/{canal_id}=s68-c-k-c0x00ffffff-no-rj",
            "thumbnail": thumbnail,
            "link": f"https://www.youtube.com/watch?v={video_id}",
            "views": views,
            "views_por_hora": int(views / max(1, ((datetime.utcnow() - parser.isoparse(publicado_em)).total_seconds() / 3600))),
            "cpm_estimado": f"R$ {cpm:.2f}",
            "receita_estimada": f"R$ {receita:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            "engajamento": engajamento,
            "duracao": duracao,
            "tempo_publicacao": tempo,
            "hashtags": "#video #trending #viral"  # Simulação
        })

    return resultados