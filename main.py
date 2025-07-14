
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import amazon_scraper, youtube

app = FastAPI()

app.include_router(amazon_scraper.router, prefix="/amazon")
app.include_router(youtube.router, prefix="/youtube")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"mensagem": "API YouTube + Amazon Online com HMAC"}
