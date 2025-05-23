import base64
import json
import os
import time
from datetime import datetime

import pandas as pd
import requests


def obtener_datos_alhambra_sharan():

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "es-ES,es;q=0.7",
        "content-type": "application/json",
        "origin": "https://www.coches.net",
        "priority": "u=1, i",
        "referer": "https://www.coches.net/",
        "sec-ch-ua": '"Chromium";v="130", "Brave";v="130", "Not?A_Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "x-adevinta-amcvid": "62034978869742262140131781523214745379",
        "x-adevinta-channel": "web-desktop",
        "x-adevinta-page-url": "https://www.coches.net/search/",
        "x-adevinta-referer": "https://www.coches.net/citroen-berlingo-talla-xl-bluehdi-100-ss-shine-7-plazas-5p-diesel-2020-en-madrid-58688598-covo.aspx",
        "x-adevinta-session-id": "2ba44881-e077-4f5c-9c13-5d23f4af9c60",
        "x-schibsted-tenant": "coches",
    }

    json_data = {
        "pagination": {
            "page": 1,
            "size": 30,
        },
        "sort": {
            "order": "desc",
            "term": "relevance",
        },
        "filters": {
            "price": {
                "from": None,
                "to": None,
            },
            "priceRank": [],
            "batteryCapacity": {
                "from": None,
                "to": None,
            },
            "bodyTypeIds": [],
            "categories": {
                "category1Ids": [
                    2500,
                ],
            },
            "chargingTimeFastMode": {
                "from": None,
                "to": None,
            },
            "chargingTimeStandardMode": {
                "from": None,
                "to": None,
            },
            "contractId": 0,
            "drivenWheelsIds": [],
            "electricAutonomy": {
                "from": None,
                "to": None,
            },
            "entry": None,
            "environmentalLabels": [],
            "equipments": [],
            "fuelTypeIds": [],
            "hasPhoto": None,
            "hasStock": None,
            "hasWarranty": None,
            "hp": {
                "from": None,
                "to": None,
            },
            "isCertified": False,
            "km": {
                "from": None,
                "to": None,
            },
            "luggageCapacity": {
                "from": None,
                "to": None,
            },
            "maxTerms": None,
            "onlyPeninsula": False,
            "offerTypeIds": [
                0,
                1,
                2,
                3,
                4,
                5,
            ],
            "provinceIds": [],
            "rating": {
                "from": None,
                "to": None,
            },
            "searchText": None,
            "seats": {
                "from": 7,
                "to": 7,
            },
            "sellerTypeId": 0,
            "transmissionTypeId": 0,
            "year": {
                "from": 2018,
                "to": None,
            },
        },
    }

    MAX_PAGE = 112
    all_info = []

    for page in range(1, MAX_PAGE + 1):
        json_data = {
            "pagination": {"page": page, "size": 30},
            "sort": {"order": "desc", "term": "relevance"},
            "filters": {
                "price": {"from": None, "to": None},
                "priceRank": [],
                "batteryCapacity": {"from": None, "to": None},
                "bodyTypeIds": [],
                "categories": {"category1Ids": [2500]},
                "chargingTimeFastMode": {"from": None, "to": None},
                "chargingTimeStandardMode": {"from": None, "to": None},
                "contractId": 0,
                "drivenWheelsIds": [],
                "electricAutonomy": {"from": None, "to": None},
                "entry": None,
                "environmentalLabels": [],
                "equipments": [],
                "fuelTypeIds": [1],
                "hasPhoto": None,
                "hasOnlineFinancing": None,
                "hasReservation": None,
                "hasStock": None,
                "hasWarranty": None,
                "hp": {"from": None, "to": None},
                "isCertified": False,
                "km": {"from": None, "to": 120000},
                "luggageCapacity": {"from": None, "to": None},
                "maxTerms": None,
                "onlyPeninsula": False,
                "offerTypeIds": [0, 1, 2, 3, 4, 5],
                "provinceIds": [],
                "rating": {"from": None, "to": None},
                "searchText": None,
                "sellerTypeId": 0,
                "transmissionTypeId": 0,
                "vehicles": [
                    {"make": "SEAT", "makeId": 39, "model": "Alhambra", "modelId": 341},
                    {
                        "make": "VOLKSWAGEN",
                        "makeId": 47,
                        "model": "Sharan",
                        "modelId": 346,
                    },
                ],
                "year": {"from": 2020, "to": None},
            },
        }

        response = requests.post(
            "https://web.gw.coches.net/search/listing",
            headers=headers,
            json=json_data,
            timeout=60,
        )
        items = response.json()["items"]
        all_info += items
        time.sleep(0.5)
        if page % 50 == 0:
            print(page)
    # Note: json_data will not be serialized by requests
    # exactly as it was in the original request.
    # data = '{"pagination":{"page":1,"size":30},"sort":{"order":"desc","term":"relevance"},"filters":{"price":{"from":null,"to":null},"priceRank":[],"batteryCapacity":{"from":null,"to":null},"bodyTypeIds":[],"categories":{"category1Ids":[2500]},"chargingTimeFastMode":{"from":null,"to":null},"chargingTimeStandardMode":{"from":null,"to":null},"contractId":0,"drivenWheelsIds":[],"electricAutonomy":{"from":null,"to":null},"entry":null,"environmentalLabels":[],"equipments":[],"fuelTypeIds":[],"hasPhoto":null,"hasStock":null,"hasWarranty":null,"hp":{"from":null,"to":null},"isCertified":false,"km":{"from":null,"to":null},"luggageCapacity":{"from":null,"to":null},"maxTerms":null,"onlyPeninsula":false,"offerTypeIds":[0,1,2,3,4,5],"provinceIds":[],"rating":{"from":null,"to":null},"searchText":null,"seats":{"from":7,"to":null},"sellerTypeId":0,"transmissionTypeId":0,"year":{"from":null,"to":null}}}'
    # response = requests.post('https://web.gw.coches.net/search/listing', headers=headers, data=data)

    with open("output_alhambra_sharan.json", "w", encoding="utf-8") as f:
        json.dump(all_info, f)

    with open("output_alhambra_sharan.json", encoding="utf-8") as f:
        data = json.load(f)

    data_cleaned = dict()
    fecha = datetime.now().strftime("%Y-%m-%d")
    for elem in data:
        new_elem = {
            elem["id"]: {
                "title": elem["title"],
                "year": elem["year"],
                "km": elem["km"],
                "price": elem["price"]["amount"],
                "date": fecha,
                "url": "https://www.coches.net" + str(elem["url"]),
            }
        }
        data_cleaned.update(new_elem)

    df_cleaned = pd.DataFrame.from_dict(data_cleaned, orient="index")
    return df_cleaned


# Configuración de GitHub y otras variables
BRANCH = "main"
GITHUB_REPO = "Quejicus/coches"  # Repositorio de GitHub
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Token de acceso personal de GitHub
CSV_PATH = (
    "data/alhambra_sharan_hist.csv"  # Ruta donde se guardará el CSV en el repositorio
)
CSV_RAW_URL = "https://raw.githubusercontent.com/Quejicus/coches/refs/heads/main/data/alhambra_sharan_hist.csv"  # URL del CSV en el repositorio de GitHub


# Función para descargar el archivo CSV desde GitHub
def download_csv_from_github():
    try:
        df = pd.read_csv(CSV_RAW_URL, encoding="utf-8", sep=",")
        print("✅ CSV descargado correctamente desde GitHub.")
        return df
    except Exception:
        print(
            "⚠️ No se pudo descargar el CSV desde GitHub. Se usará un DataFrame vacío."
        )
        return pd.DataFrame()


# Función para guardar el archivo CSV en GitHub
def upload_csv_to_github(df, commit_message):
    # Convertir el DataFrame en CSV
    csv_data = df.to_csv(index=False)
    encoded_csv = base64.b64encode(csv_data.encode("utf-8")).decode("utf-8")

    # Crear la URL de la API de GitHub para cargar el archivo CSV
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{CSV_PATH}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    sha = get_file_sha()

    data = {"message": commit_message, "content": encoded_csv, "branch": BRANCH}

    if sha:
        data["sha"] = sha  # Necesario para actualizar un archivo existente

    response = requests.put(url, json=data, headers=headers, timeout=60)

    if response.status_code in [200, 201]:
        print("✅ CSV actualizado y subido a GitHub correctamente.")
    else:
        print(f"❌ Error al subir el archivo: {response.status_code}")
        print(response.text)


def get_file_sha():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{CSV_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code == 200:
        return response.json()["sha"]
    else:
        return None


def update_csv():
    df_existing = download_csv_from_github()
    df_new = obtener_datos_alhambra_sharan()
    df_new.reset_index(inplace=True, names="id")

    # Ensure the 'url' column exists in both DataFrames
    if "url" not in df_existing.columns:
        df_existing["url"] = None

    # Concatenate the new data with the existing data
    df_concat = pd.concat([df_existing, df_new], ignore_index=True)
    df_concat.drop_duplicates(subset=["id", "date"], inplace=True)

    # Guardar el CSV concatenado en GitHub
    commit_message = f"Actualizar histórico de CSV con nuevos datos - {datetime.today().strftime('%Y-%m-%d')}"
    upload_csv_to_github(df_concat, commit_message)


if __name__ == "__main__":
    update_csv()
