from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import youtube_detalhado, amazon_detalhado

app = FastAPI()

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(youtube_detalhado.router, prefix="/youtube")
app.include_router(amazon_detalhado.router, prefix="/amazon")
