#!/usr/bin/env python3

from datetime import datetime
import json
import os
from pathlib import Path


EXCLUDE_FIELDS = (
    "system_Serial",
    "system_Version",
    "system_RSSI",
    "system_MAC",
    "system_IP",
)


def exclude(d: dict, fields: list[str]) -> dict:
    return {k: v for k, v in d.items() if k not in fields}


def exclude_endswith(d: dict, fields: list[str]) -> dict:
    return {
        k: v for k, v in d.items() if all(not k.endswith(f) for f in fields)
    }


def convert_if_possible(val: str) -> str | float | int:
    # EAFP
    try:
        return float(val)
    except ValueError:
        pass
    return val


def convert_values(d: dict) -> dict:
    return {k: convert_if_possible(v) for k, v in d.items()}


def fix(orig: dict) -> dict:
    data = exclude(orig["data"], EXCLUDE_FIELDS)
    data = exclude_endswith(data, ["calibr_date"])
    data = convert_values(data)
    return {
        "date": orig["Date"],
        "serial": orig["serial"],
        "name": orig["uName"],
        "data": data,
    }

def unite(path: Path, outfile: Path) -> None:
    dataset = []
    for file in os.listdir(path):
        print(f"Processing {file}")
        with open(path / file, "r") as fp:
            data = json.load(fp)
        for v in data.values():
            dataset.append(fix(v))
    dataset.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d %H:%M:%S"))
    with outfile.open("w") as fp:
        json.dump(dataset, fp, ensure_ascii=False)

unite(Path("loaded").resolve(), Path("dataset.json"))
