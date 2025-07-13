
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import amazon_router
import os

app = FastAPI()

# CORS liberado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(amazon_router.router, prefix="/amazon")

@app.get("/")
def root():
    return {"status": "API ativa"}
