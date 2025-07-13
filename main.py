from fastapi import FastAPI
from routers import youtube_busca, amazon_busca

app = FastAPI()

app.include_router(youtube_busca.router, prefix="/youtube")
app.include_router(amazon_busca.router, prefix="/amazon")