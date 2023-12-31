#!/usr/bin/env python3
from datetime import datetime, timedelta
import json
from pathlib import Path
from typing import Any
import requests


START = datetime(year=2022, month=7, day=31)
N_DAYS = 6
DIR = Path(__file__).resolve().parent / "raw_data"
DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "http://webrobo.mgul.ac.ru:3000/db_api_REST/calibr"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
}


def get_sensors_data(day: datetime) -> Any:
    fmt = day.strftime("%Y-%m-%d")
    url = f"{BASE_URL}/day/{fmt}"
    response = requests.get(url, headers=HEADERS)
    return response.json()


for i in range(N_DAYS):
    date = START + timedelta(days=i)

    print(date.strftime("Processing %d/%m/%Y"))
    data = get_sensors_data(date)

    file = DIR / date.strftime("%Y-%m-%d.json")
    with file.open("w") as fp:
        json.dump(data, fp, indent=2, ensure_ascii=False)
    print(f"File {file} saved")
