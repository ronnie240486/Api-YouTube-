
import os
import datetime
import hashlib
import hmac
import requests

def buscar_produtos_amazon(termo):
    access_key = os.getenv("AWS_ACCESS_KEY")
    secret_key = os.getenv("AWS_SECRET_KEY")
    partner_tag = os.getenv("AMAZON_TAG")
    region = os.getenv("REGION", "us-east-1")

    if not all([access_key, secret_key, partner_tag]):
        raise ValueError("Credenciais da Amazon não estão definidas no .env")

    host = f"webservices.amazon.{region.split('-')[0]}.com"
    endpoint = f"https://{host}/paapi5/searchitems"

    payload = {
        "Keywords": termo,
        "Resources": [
            "Images.Primary.Large",
            "ItemInfo.Title",
            "Offers.Listings.Price"
        ],
        "PartnerTag": partner_tag,
        "PartnerType": "Associates",
        "Marketplace": "www.amazon.com"
    }

    headers = gerar_headers_amazon(payload, access_key, secret_key, region, host)
    response = requests.post(endpoint, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Erro Amazon API: {response.status_code} - {response.text}")

    data = response.json()
    itens = data.get("SearchResult", {}).get("Items", [])
    resultado = []

    for item in itens:
        resultado.append({
            "titulo": item.get("ItemInfo", {}).get("Title", {}).get("DisplayValue", "Sem título"),
            "imagem": item.get("Images", {}).get("Primary", {}).get("Large", {}).get("URL"),
            "preco": item.get("Offers", {}).get("Listings", [{}])[0].get("Price", {}).get("DisplayAmount", "N/A")
        })

    return resultado

def gerar_headers_amazon(payload, access_key, secret_key, region, host):
    import json
    amz_target = "com.amazon.paapi5.v1.ProductAdvertisingAPIv1.SearchItems"
    content = json.dumps(payload)
    content_type = "application/json; charset=UTF-8"
    amz_date = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    datestamp = datetime.datetime.utcnow().strftime("%Y%m%d")
    canonical_uri = "/paapi5/searchitems"
    canonical_headers = f"content-encoding:utf-8\ncontent-type:{content_type}\nhost:{host}\nx-amz-date:{amz_date}\nx-amz-target:{amz_target}\n"
    signed_headers = "content-encoding;content-type;host;x-amz-date;x-amz-target"
    payload_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    canonical_request = f"POST\n{canonical_uri}\n\n{canonical_headers}\n{signed_headers}\n{payload_hash}"
    algorithm = "AWS4-HMAC-SHA256"
    credential_scope = f"{datestamp}/{region}/ProductAdvertisingAPI/aws4_request"
    string_to_sign = f"{algorithm}\n{amz_date}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"
    signing_key = get_signature_key(secret_key, datestamp, region, "ProductAdvertisingAPI")
    signature = hmac.new(signing_key, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

    authorization_header = (
        f"{algorithm} Credential={access_key}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, Signature={signature}"
    )

    headers = {
        "Content-Encoding": "utf-8",
        "Content-Type": content_type,
        "X-Amz-Date": amz_date,
        "X-Amz-Target": amz_target,
        "Authorization": authorization_header,
        "Host": host
    }

    return headers

def get_signature_key(key, date_stamp, region_name, service_name):
    def sign(k, msg):
        return hmac.new(k, msg.encode("utf-8"), hashlib.sha256).digest()

    k_date = sign(("AWS4" + key).encode("utf-8"), date_stamp)
    k_region = sign(k_date, region_name)
    k_service = sign(k_region, service_name)
    k_signing = sign(k_service, "aws4_request")
    return k_signing
