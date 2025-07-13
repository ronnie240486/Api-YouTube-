
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "API Online"}

@app.get("/amazon/testar")
def testar_variaveis():
    access_key = os.getenv("AWS_ACCESS_KEY")
    secret_key = os.getenv("AWS_SECRET_KEY")
    tag = os.getenv("AMAZON_TAG")
    endpoint = os.getenv("ENDPOINT")
    region = os.getenv("REGION")
    return {
        "AWS_ACCESS_KEY": access_key,
        "AWS_SECRET_KEY": "✔️" if secret_key else None,
        "AMAZON_TAG": tag,
        "ENDPOINT": endpoint,
        "REGION": region
    }
