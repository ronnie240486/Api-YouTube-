
import os
from typing import List
import datetime
from amazon.paapi import AmazonAPI

def buscar_produtos_reais(termo: str) -> List[dict]:
    access_key = os.getenv("AWS_ACCESS_KEY")
    secret_key = os.getenv("AWS_SECRET_KEY")
    associate_tag = os.getenv("AMAZON_TAG")
    region = os.getenv("REGION", "us-east-1")

    if not all([access_key, secret_key, associate_tag]):
        raise ValueError("Credenciais da Amazon não estão definidas no .env")

    amazon = AmazonAPI(access_key, secret_key, associate_tag, region)
    products = amazon.search_items(keywords=termo, search_index="All", item_count=10)

    resultados = []
    for item in products.items:
        resultados.append({
            "titulo": item.item_info.title.display_value,
            "preco": getattr(item.offers.listings[0].price, "display_amount", "R$ ?"),
            "imagem": item.images.primary.large.url,
            "avaliacao": item.item_info.by_line_info.brand.display_value if item.item_info.by_line_info else "N/A",
            "link": item.detail_page_url
        })
    return resultados
