
from fastapi import APIRouter, Query
import httpx
from bs4 import BeautifulSoup

router = APIRouter()

@router.get("/buscar")
async def buscar_produtos(termo: str = Query(...)):
    url = f"https://www.amazon.com.br/s?k={termo.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "lxml")

    produtos = []
    for item in soup.select(".s-result-item")[:5]:
        nome = item.select_one("h2 span")
        imagem = item.select_one("img")
        preco = item.select_one(".a-price span")
        link = item.select_one("h2 a")

        if nome and imagem and preco and link:
            produtos.append({
                "nome": nome.text.strip(),
                "imagem": imagem["src"],
                "preco": preco.text.strip(),
                "link": f"https://www.amazon.com.br{link['href']}"
            })

    return {"produtos": produtos}
