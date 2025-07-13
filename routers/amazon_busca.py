from fastapi import APIRouter, Query
from typing import Optional
import datetime, hashlib, hmac, requests
from urllib.parse import quote
from routers.amazon_config import AWS_ACCESS_KEY, AWS_SECRET_KEY, ASSOCIATE_TAG, REGION, MARKETPLACE

router = APIRouter()

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def get_signature_key(key, date_stamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

@router.get("/buscar")
def buscar_produtos(termo: str, categoria: Optional[str] = None):
    method = 'GET'
    service = 'ProductAdvertisingAPI'
    host = MARKETPLACE
    endpoint = f"https://{host}/paapi5/searchitems"

    t = datetime.datetime.utcnow()
    amz_date = t.strftime('%Y%m%dT%H%M%SZ')
    date_stamp = t.strftime('%Y%m%d')

    canonical_uri = '/paapi5/searchitems'
    canonical_querystring = ''
    payload = {
        "Keywords": termo,
        "SearchIndex": "All",
        "Resources": [
            "Images.Primary.Medium",
            "ItemInfo.Title",
            "ItemInfo.ByLineInfo",
            "Offers.Listings.Price",
            "CustomerReviews.Count",
            "CustomerReviews.StarRating"
        ],
        "PartnerTag": ASSOCIATE_TAG,
        "PartnerType": "Associates",
        "Marketplace": "www.amazon.com.br"
    }

    import json
    payload_json = json.dumps(payload)

    canonical_headers = f"content-encoding:utf-8\ncontent-type:application/json; charset=utf-8\nhost:{host}\nx-amz-date:{amz_date}\n"
    signed_headers = 'content-encoding;content-type;host;x-amz-date'
    payload_hash = hashlib.sha256(payload_json.encode('utf-8')).hexdigest()

    canonical_request = f"{method}\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{payload_hash}"
    algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = f"{date_stamp}/{REGION}/{service}/aws4_request"
    string_to_sign = f"{algorithm}\n{amz_date}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"

    signing_key = get_signature_key(AWS_SECRET_KEY, date_stamp, REGION, service)
    signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

    headers = {
        'Content-Encoding': 'utf-8',
        'Content-Type': 'application/json; charset=utf-8',
        'Host': host,
        'X-Amz-Date': amz_date,
        'Authorization': f"{algorithm} Credential={AWS_ACCESS_KEY}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}"
    }

    try:
        response = requests.post(endpoint, headers=headers, data=payload_json)
        data = response.json()
        produtos = []

        for item in data.get("SearchResult", {}).get("Items", []):
            produtos.append({
                "nome": item["ItemInfo"]["Title"]["DisplayValue"],
                "preco": item["Offers"]["Listings"][0]["Price"]["DisplayAmount"],
                "avaliacao": item.get("CustomerReviews", {}).get("StarRating", {}).get("DisplayValue", "N/A"),
                "imagem": item["Images"]["Primary"]["Medium"]["URL"],
                "link": item["DetailPageURL"]
            })

        return {"produtos": produtos}

    except Exception as e:
        return {"erro": str(e)}