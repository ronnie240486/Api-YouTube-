
import os
import time
import hmac
import hashlib
import base64
import httpx
from fastapi import APIRouter, Query
from urllib.parse import quote, urlencode
import xml.etree.ElementTree as ET

router = APIRouter()

ACCESS_KEY = "AKPAFS7GN91752367329"
SECRET_KEY = "LgObq/8bWan5cBlurvvghdOIyM/QP9mFvqnPn1RQ"
PARTNER_TAG = "casaedecor0a8-20"
REGION = "us-east-1"
HOST = "webservices.amazon.com.br"
SERVICE = "ProductAdvertisingAPI"
ENDPOINT = f"https://{HOST}/paapi5/searchitems"

def sign(headers, payload):
    method = "POST"
    canonical_uri = "/paapi5/searchitems"
    canonical_headers = "content-encoding:amz-1.0\nhost:" + HOST + "\nx-amz-date:" + headers["x-amz-date"] + "\n"
    signed_headers = "content-encoding;host;x-amz-date"
    payload_hash = hashlib.sha256(payload.encode()).hexdigest()
    canonical_request = f"{method}\n{canonical_uri}\n\n{canonical_headers}\n{signed_headers}\n{payload_hash}"

    date = headers["x-amz-date"][:8]
    k_date = hmac.new(("AWS4" + SECRET_KEY).encode(), date.encode(), hashlib.sha256).digest()
    k_region = hmac.new(k_date, REGION.encode(), hashlib.sha256).digest()
    k_service = hmac.new(k_region, SERVICE.encode(), hashlib.sha256).digest()
    k_signing = hmac.new(k_service, b"aws4_request", hashlib.sha256).digest()
    signature = hmac.new(k_signing, canonical_request.encode(), hashlib.sha256).hexdigest()

    authorization = (
        f"AWS4-HMAC-SHA256 Credential={ACCESS_KEY}/{date}/{REGION}/{SERVICE}/aws4_request, "
        f"SignedHeaders={signed_headers}, Signature={signature}"
    )

    headers["Authorization"] = authorization
    return headers

@router.get("/buscar")
async def buscar_amazon(termo: str = Query(...)):
    payload = f'''
    {{
        "Keywords": "{termo}",
        "Resources": [
            "Images.Primary.Medium",
            "ItemInfo.Title",
            "Offers.Listings.Price"
        ],
        "PartnerTag": "{PARTNER_TAG}",
        "PartnerType": "Associates",
        "Marketplace": "www.amazon.com.br"
    }}
    '''

    t = time.gmtime()
    amzdate = time.strftime("%Y%m%dT%H%M%SZ", t)

    headers = {
        "content-encoding": "amz-1.0",
        "content-type": "application/json; charset=utf-8",
        "host": HOST,
        "x-amz-date": amzdate,
    }

    headers = sign(headers, payload)

    async with httpx.AsyncClient() as client:
        response = await client.post(ENDPOINT, headers=headers, content=payload)

    if response.status_code != 200:
        return {"erro": f"Erro na API Amazon: {response.status_code}"}

    data = response.json()
    produtos = []
    for item in data.get("SearchResult", {}).get("Items", []):
        produto = {
            "nome": item["ItemInfo"]["Title"]["DisplayValue"],
            "imagem": item["Images"]["Primary"]["Medium"]["URL"],
            "preco": item["Offers"]["Listings"][0]["Price"]["DisplayAmount"] if item.get("Offers") else "N/A",
            "link": item.get("DetailPageURL", "#")
        }
        produtos.append(produto)

    return {"produtos": produtos[:5]}
