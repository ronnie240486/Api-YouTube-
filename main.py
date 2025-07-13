from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import buscar_videos

app = FastAPI()

# Ativando CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou substitua por ['https://seusite.netlify.app'] para mais segurança
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(buscar_videos.router, prefix="/youtube")