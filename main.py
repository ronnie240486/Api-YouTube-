from fastapi import FastAPI
from routers import youtube_scraper, amazon_scraper
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(youtube_scraper.router)
app.include_router(amazon_scraper.router)

@app.get("/")
def root():
    return {"mensagem": "✅ API YouTube + Amazon Online com HMAC"}
