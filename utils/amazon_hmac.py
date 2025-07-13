
import os
import json
import requests
import datetime
import hashlib
import hmac
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AMAZON_TAG = os.getenv("AMAZON_TAG")
REGION = os.getenv("REGION", "us-east-1")
SERVICE = "ProductAdvertisingAPI"
HOST = os.getenv("ENDPOINT", "webservices.amazon.com.br").replace("https://", "")
ENDPOINT = f"https://{HOST}/paapi5/searchitems"

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def get_signature_key(key, date_stamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning

def buscar_produtos_amazon(termo):
    if not AWS_ACCESS_KEY or not AWS_SECRET_KEY or not AMAZON_TAG:
        raise Exception("Credenciais da Amazon não estão definidas no .env")

    t = datetime.datetime.utcnow()
    amz_date = t.strftime('%Y%m%dT%H%M%SZ')
    date_stamp = t.strftime('%Y%m%d')  # Date w/o time, used in credential scope

    payload = {
        "Keywords": termo,
        "SearchIndex": "All",
        "ItemCount": 10,
        "Resources": [
            "Images.Primary.Large",
            "ItemInfo.Title",
            "Offers.Listings.Price",
            "Offers.Listings.SavingBasis",
            "ItemInfo.ByLineInfo",
            "CustomerReviews.Count",
            "CustomerReviews.StarRating",
            "Offers.Listings.MerchantInfo",
            "BrowseNodeInfo.BrowseNodes"
        ],
        "PartnerTag": AMAZON_TAG,
        "PartnerType": "Associates",
        "Marketplace": "www.amazon.com.br"
    }

    headers = {
        "content-encoding": "amz-1.0",
        "content-type": "application/json; charset=UTF-8",
        "host": HOST,
        "x-amz-date": amz_date
    }

    canonical_uri = "/paapi5/searchitems"
    canonical_querystring = ""
    canonical_headers = f"content-encoding:amz-1.0\ncontent-type:application/json; charset=UTF-8\nhost:{HOST}\nx-amz-date:{amz_date}\n"
    signed_headers = "content-encoding;content-type;host;x-amz-date"
    payload_hash = hashlib.sha256(json.dumps(payload).encode('utf-8')).hexdigest()
    canonical_request = f"POST\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{payload_hash}"

    algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = f"{date_stamp}/{REGION}/{SERVICE}/aws4_request"
    string_to_sign = f"{algorithm}\n{amz_date}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"

    signing_key = get_signature_key(AWS_SECRET_KEY, date_stamp, REGION, SERVICE)
    signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

    authorization_header = f"{algorithm} Credential={AWS_ACCESS_KEY}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}"
    headers["Authorization"] = authorization_header

    response = requests.post(ENDPOINT, headers=headers, data=json.dumps(payload), timeout=15)
    data = response.json()

    produtos = []
    for item in data.get("SearchResult", {}).get("Items", []):
        produto = {
            "titulo": item.get("ItemInfo", {}).get("Title", {}).get("DisplayValue", "Sem título"),
            "imagem": item.get("Images", {}).get("Primary", {}).get("Large", {}).get("URL", ""),
            "preco": item.get("Offers", {}).get("Listings", [{}])[0].get("Price", {}).get("DisplayAmount", "Indisponível"),
            "avaliacao": item.get("CustomerReviews", {}).get("StarRating", {}).get("DisplayValue", "0"),
            "avaliacoes": item.get("CustomerReviews", {}).get("Count", 0),
            "link": item.get("DetailPageURL", "#")
        }
        produtos.append(produto)

    return produtos
