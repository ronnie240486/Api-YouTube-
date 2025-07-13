
from fastapi import FastAPI
from routers import youtube_real, amazon_paapi

app = FastAPI()

app.include_router(youtube_real.router, prefix="/youtube")
app.include_router(amazon_paapi.router, prefix="/amazon")
