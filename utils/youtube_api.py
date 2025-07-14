import requests
import os

API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"

def buscar_videos(termo, pais="BR"):
    params = {
        "part": "snippet",
        "q": termo,
        "regionCode": pais,
        "type": "video",
        "maxResults": 10,
        "key": API_KEY
    }
    r = requests.get(YOUTUBE_API_URL, params=params)
    if r.status_code != 200:
        return {"erro": "Erro ao buscar vídeos"}
    return r.json()
