from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import amazon_scraper, youtube_viralizar

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(amazon_scraper.router, prefix="/amazon")
app.include_router(youtube_viralizar.router, prefix="/youtube")

@app.get("/")
def read_root():
    return {"status": "API ativa: YouTube + Amazon"}
