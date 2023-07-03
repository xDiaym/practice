#!/usr/bin/env python3
import sys
from collections import defaultdict
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
        **data,
    }


def unite(path: Path, outdir: Path) -> None:
    gadgets = defaultdict(list)
    for file in os.listdir(path):
        print(f"Reading {file}")
        if Path(file).is_dir():
            continue
        with open(path / file, "r") as fp:
            data = json.load(fp)
        for v in data.values():
            assert "uName" in v
            gadgets[v["uName"]].append(fix(v))

    os.makedirs(outdir, exist_ok=True)

    for gadget_name, values in gadgets.items():
        if sys.platform == 'win32':
            gadget_name = gadget_name.encode('cp1251').decode('utf-8')
        print(f"Processing {gadget_name}")
        values.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d %H:%M:%S"))
        outfile = outdir / f"{gadget_name}.json"
        with outfile.open("w") as fp:
            json.dump(values, fp, ensure_ascii=False)


unite(Path("../raw_data").resolve(), Path("../datasets").resolve())
