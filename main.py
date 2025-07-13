from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import youtube_busca, amazon_busca

app = FastAPI()

# CORS liberado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Substituir por domínio Netlify se desejar restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(youtube_busca.router, prefix="/youtube")
app.include_router(amazon_busca.router, prefix="/amazon")
