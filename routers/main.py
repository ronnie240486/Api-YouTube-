from fastapi import FastAPI
from routers import amazon_scraper

app = FastAPI()

app.include_router(amazon_scraper.router, prefix="/amazon")