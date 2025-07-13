
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from routers import amazon_scraper, youtube_scraper

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(amazon_scraper.router)
app.include_router(youtube_scraper.router)

@app.get("/")
def root():
    return {"status": "API Online"}
