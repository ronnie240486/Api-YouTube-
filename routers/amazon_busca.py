
from fastapi import APIRouter, Query
from dotenv import load_dotenv
import os, requests, hashlib, hmac, datetime, base64
import xml.etree.ElementTree as ET

router = APIRouter()

load_dotenv()

ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
TAG = os.getenv("ASSOCIATE_TAG")
REGION = os.getenv("REGION")
HOST = os.getenv("MARKETPLACE")
SERVICE = "ProductAdvertisingAPI"
ENDPOINT = f"https://{HOST}/paapi5/searchitems"

def sign_request(payload):
    amz_date = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    date_stamp = datetime.datetime.utcnow().strftime('%Y%m%d')
    canonical_uri = "/paapi5/searchitems"
    canonical_headers = f"host:{HOST}\n"
    signed_headers = "host"
    algorithm = "AWS4-HMAC-SHA256"
    credential_scope = f"{date_stamp}/{REGION}/{SERVICE}/aws4_request"

    canonical_request = f"POST\n{canonical_uri}\n\n{canonical_headers}\n{signed_headers}\n{hashlib.sha256(payload.encode()).hexdigest()}"
    string_to_sign = f"{algorithm}\n{amz_date}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode()).hexdigest()}"

    def sign(key, msg): return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()
    k_date = sign(("AWS4" + SECRET_KEY).encode(), date_stamp)
    k_region = sign(k_date, REGION)
    k_service = sign(k_region, SERVICE)
    k_signing = sign(k_service, "aws4_request")
    signature = hmac.new(k_signing, string_to_sign.encode(), hashlib.sha256).hexdigest()

    authorization = f"{algorithm} Credential={ACCESS_KEY}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-Amz-Date": amz_date,
        "Authorization": authorization,
        "Host": HOST,
    }
    return headers

@router.get("/buscar")
def buscar_produtos(termo: str = Query(...)):
    payload = f'''{{
      "Keywords": "{termo}",
      "SearchIndex": "All",
      "Resources": [
        "Images.Primary.Medium",
        "ItemInfo.Title",
        "Offers.Listings.Price",
        "CustomerReviews.Count",
        "CustomerReviews.StarRating"
      ],
      "PartnerTag": "{TAG}",
      "PartnerType": "Associates",
      "Marketplace": "www.amazon.com.br"
    }}'''

    headers = sign_request(payload)

    response = requests.post(ENDPOINT, data=payload.encode("utf-8"), headers=headers)
    try:
        data = response.json()
        produtos = []
        for item in data.get("SearchResult", {}).get("Items", []):
            produtos.append({
                "nome": item["ItemInfo"]["Title"]["DisplayValue"],
                "preco": item.get("Offers", {}).get("Listings", [{}])[0].get("Price", {}).get("DisplayAmount", "N/A"),
                "imagem": item.get("Images", {}).get("Primary", {}).get("Medium", {}).get("URL", ""),
                "avaliacao": item.get("CustomerReviews", {}).get("StarRating", {}).get("DisplayValue", "Sem avaliação"),
                "link": item.get("DetailPageURL", "#")
            })
        return {"produtos": produtos}
    except Exception as e:
        return {"erro": str(e)}
