from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import youtube_real, amazon_real

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(youtube_real.router, prefix="/youtube")
app.include_router(amazon_real.router, prefix="/amazon")
