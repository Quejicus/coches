import datetime
import json
import os
import time

import pandas as pd
import requests
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

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
                {"make": "VOLKSWAGEN", "makeId": 47, "model": "Sharan", "modelId": 346},
            ],
            "year": {"from": 2020, "to": None},
        },
    }

    response = requests.post(
        "https://web.gw.coches.net/search/listing", headers=headers, json=json_data
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

with open("output_alhambra_sharan.json") as f:
    data = json.load(f)

data_cleaned = dict()
fecha = datetime.datetime.now().strftime("%Y-%m-%d")
for elem in data:
    new_elem = {
        elem["id"]: {
            "title": elem["title"],
            "year": elem["year"],
            "km": elem["km"],
            "price": elem["price"]["amount"],
            "date": fecha,
        }
    }
    data_cleaned.update(new_elem)

df_cleaned = pd.DataFrame.from_dict(data_cleaned, orient="index")

HISTORICO_FILE = "alhambra_sharan_hist.csv"

if os.path.exists(HISTORICO_FILE):
    df_existing = pd.read_csv(HISTORICO_FILE)
    df_combined = pd.concat([df_existing, df_cleaned], ignore_index=True)
else:
    df_combined = df_cleaned

df_combined.to_csv(HISTORICO_FILE, index=True, index_label="id")

gauth = GoogleAuth()
gauth.LoadCredentialsFile("mycreds.txt")

if gauth.credentials is None:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()

gauth.SaveCredentialsFile("mycreds.txt")
drive = GoogleDrive(gauth)

# === 5. Subir archivo a Google Drive (sobrescribe historico.csv) ===
file_drive = drive.CreateFile({"title": "historico.csv"})
file_drive.SetContentFile(HISTORICO_FILE)
file_drive.Upload()

print("✅ Archivo histórico actualizado y subido a Google Drive.")
