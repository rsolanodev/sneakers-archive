import os
import re
import unicodedata
from typing import List

import requests


def download_image(brand_folder: str, url: str) -> None:
    filename = url.split("/")[-1]
    response = requests.get(url, stream=True)
    if response.ok:
        with open(f"{brand_folder}/{filename}", "wb") as fd:
            for chunk in response.iter_content(chunk_size=1024):
                fd.write(chunk)


def download_images(brand: str, sneakers: List) -> None:
    if not os.path.exists("images"):
        os.mkdir("images")
    brand_folder = slugify(value=brand)
    brand_folder_path = f"images/{brand_folder}"
    if not os.path.exists(brand_folder_path):
        os.mkdir(brand_folder_path)
    for sneaker in sneakers:
        download_image(brand_folder=brand_folder_path, url=sneaker["image"])


def slugify(value: str, allow_unicode: bool = False) -> str:
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")
