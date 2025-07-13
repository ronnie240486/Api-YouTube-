from fastapi import APIRouter, Query
import datetime
import hashlib
import hmac
import requests
from urllib.parse import quote, urlencode

router = APIRouter()

ACCESS_KEY = "AKPAFS7GN91752367329"
SECRET_KEY = "LgObq/8bWan5cBlurvvghdOIyM/QP9mFvqnPn1RQ"
PARTNER_TAG = "casaedecor0a8-20"
REGION = "us-east-1"
HOST = "webservices.amazon.com.br"
ENDPOINT = f"https://{HOST}/paapi5/searchitems"

@router.get("/buscar")
def buscar_produtos(termo: str = Query(..., min_length=2)):
    payload = {
        "Keywords": termo,
        "Resources": [
            "Images.Primary.Medium",
            "ItemInfo.Title",
            "Offers.Listings.Price",
            "CustomerReviews.Count",
            "CustomerReviews.StarRating"
        ],
        "PartnerTag": PARTNER_TAG,
        "PartnerType": "Associates",
        "Marketplace": "www.amazon.com.br"
    }

    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "X-Amz-Target": "com.amazon.paapi5.v1.ProductAdvertisingAPIv1.SearchItems"
    }

    # AWS assinatura HMAC será feita em backend protegido (não via client)
    return {"erro": "Conexão real com Amazon PAAPI v5 em fase final de integração segura via HMAC."}
