
from fastapi import APIRouter, Query
import os
import datetime
import hashlib
import hmac
import base64
import requests
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

def log_debug(msg):
    with open("amazon_debug.log", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {msg}\n")

@router.get("/amazon/buscar")
def buscar_amazon(termo: str = Query(...)):
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
    AMAZON_TAG = os.getenv("AMAZON_TAG")
    REGION = os.getenv("REGION", "us-east-1")

    if not AWS_ACCESS_KEY or not AWS_SECRET_KEY or not AMAZON_TAG:
        return {"erro": "Credenciais da Amazon não estão definidas no .env"}

    log_debug(f"Buscando: {termo}")

    host = "webservices.amazon.com.br"
    endpoint = f"https://{host}/paapi5/searchitems"
    headers = {
        "Content-Encoding": "amz-1.0",
        "Content-Type": "application/json; charset=utf-8",
        "Host": host,
        "X-Amz-Target": "com.amazon.paapi5.v1.ProductAdvertisingAPIv1.SearchItems"
    }

    payload = {
        "Keywords": termo,
        "SearchIndex": "All",
        "Resources": [
            "Images.Primary.Small",
            "ItemInfo.Title",
            "Offers.Listings.Price"
        ],
        "PartnerTag": AMAZON_TAG,
        "PartnerType": "Associates",
        "Marketplace": "www.amazon.com.br"
    }

    import json
    import datetime
    import requests
    import hashlib
    import hmac

    def sign(key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    def getSignatureKey(key, dateStamp, regionName, serviceName):
        kDate = sign(("AWS4" + key).encode("utf-8"), dateStamp)
        kRegion = sign(kDate, regionName)
        kService = sign(kRegion, serviceName)
        kSigning = sign(kService, "aws4_request")
        return kSigning

    method = "POST"
    service = "ProductAdvertisingAPI"
    content_type = "application/json; charset=utf-8"
    amz_target = "com.amazon.paapi5.v1.ProductAdvertisingAPIv1.SearchItems"
    request_parameters = json.dumps(payload)

    t = datetime.datetime.utcnow()
    amz_date = t.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = t.strftime("%Y%m%d")

    canonical_uri = "/paapi5/searchitems"
    canonical_querystring = ""
    canonical_headers = f"content-encoding:amz-1.0\ncontent-type:{content_type}\nhost:{host}\nx-amz-date:{amz_date}\nx-amz-target:{amz_target}\n"
    signed_headers = "content-encoding;content-type;host;x-amz-date;x-amz-target"
    payload_hash = hashlib.sha256(request_parameters.encode("utf-8")).hexdigest()

    canonical_request = f"{method}\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{payload_hash}"
    algorithm = "AWS4-HMAC-SHA256"
    credential_scope = f"{date_stamp}/{REGION}/{service}/aws4_request"
    string_to_sign = f"{algorithm}\n{amz_date}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"

    signing_key = getSignatureKey(AWS_SECRET_KEY, date_stamp, REGION, service)
    signature = hmac.new(signing_key, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

    authorization_header = (
        f"{algorithm} Credential={AWS_ACCESS_KEY}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, Signature={signature}"
    )

    headers.update({
        "X-Amz-Date": amz_date,
        "Authorization": authorization_header
    })

    try:
        response = requests.post(endpoint, headers=headers, data=request_parameters)
        log_debug(f"Status: {response.status_code}")
        log_debug(f"Response: {response.text[:500]}")  # Log parcial para não travar
        if response.status_code == 200:
            data = response.json()
            resultados = []
            for item in data.get("SearchResult", {}).get("Items", []):
                titulo = item.get("ItemInfo", {}).get("Title", {}).get("DisplayValue", "Sem título")
                preco = item.get("Offers", {}).get("Listings", [{}])[0].get("Price", {}).get("DisplayAmount", "N/A")
                imagem = item.get("Images", {}).get("Primary", {}).get("Small", {}).get("URL", "")
                resultados.append({
                    "titulo": titulo,
                    "preco": preco,
                    "imagem": imagem
                })
            return resultados or [{"erro": "Nenhum item retornado"}]
        else:
            return {"erro": f"Erro na API Amazon: {response.status_code}"}
    except Exception as e:
        log_debug(f"Erro Exception: {str(e)}")
        return {"erro": f"Erro ao buscar: {str(e)}"}
