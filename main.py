from fastapi import FastAPI
from routers import buscar_videos

app = FastAPI()
app.include_router(buscar_videos.router, prefix="/youtube")