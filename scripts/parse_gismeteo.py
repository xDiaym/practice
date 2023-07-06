#!/usr/bin/env python3
from datetime import datetime

import requests
from bs4 import BeautifulSoup

URL = "https://www.gismeteo.ru/diary/{city_code}/{year}/{month}/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
}


def scrap_weather(html: str, date: datetime) -> list[dict]:
    result = []
    soup = BeautifulSoup(html, features="html.parser")
    table = soup.find("table")
    data = table.find("tbody").findAll("tr")

    for row in data:
        day = row.findAll("td")
        date = date.replace(hour=14, day=int(day[0].text))
        result.append(
            {
                "date": date.strftime("%Y-%m-%d %H:%M:%S"),
                "temperature": int(day[1].text),
                "pressure": int(day[2].text),
            }
        )
        date = date.replace(hour=22, day=int(day[0].text))
        result.append(
            {
                "date": date.strftime("%Y-%m-%d %H:%M:%S"),
                "temperature": int(day[6].text),
                "pressure": int(day[7].text),
            }
        )
    return result


def get_weather(date: datetime, city_code: int) -> list[dict]:
    url = URL.format(city_code=city_code, year=date.year, month=date.month)
    response = requests.get(url, headers=HEADERS)
    return scrap_weather(response.text, date)


if __name__ == "__main__":
    import json
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("city_code", type=int)
    parser.add_argument("year", type=int)
    parser.add_argument("month", type=int, choices=range(1, 13))
    parser.add_argument("--outfile", "-o", help="output file")
    args = parser.parse_args()

    date = datetime(year=args.year, month=args.month, day=1)
    weather = get_weather(date, args.city_code)

    if args.outfile:
        with open(args.outfile, "w") as fp:
            json.dump(weather, fp, ensure_ascii=False, indent=2)
    else:
        print(json.dumps(weather, ensure_ascii=False, indent=2))
