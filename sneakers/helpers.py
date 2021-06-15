import os
import re
import unicodedata
from typing import Any, List, Optional

import requests

from sneakers.constants import Color


def download_image(folder: str, url: str) -> int:
    filename = url.split("/")[-1]
    if not os.path.exists(f"{folder}/{filename}"):
        response = requests.get(url, stream=True)
        if response.ok:
            with open(f"{folder}/{filename}", "wb") as fd:
                for chunk in response.iter_content(chunk_size=1024):
                    fd.write(chunk)
                message(f"New image generated in {folder}/{filename}", extra="success")
                return 1
    return 0


def download_images_by_brand(brand: str, sneakers: List) -> int:
    if not os.path.exists("images"):
        os.mkdir("images")
    brand_folder = slugify(value=brand)
    brand_folder_path = f"images/{brand_folder}"
    if not os.path.exists(brand_folder_path):
        os.mkdir(brand_folder_path)

    sneakers_downloaded: int = 0
    for sneaker in sneakers:
        success = download_image(folder=brand_folder_path, url=sneaker["image"])
        sneakers_downloaded += success
    return sneakers_downloaded


def download_images_by_date(year: str, sneakers: List) -> int:
    if not os.path.exists("images"):
        os.mkdir("images")
    date_folder_path = f"images/{year}"
    if not os.path.exists(date_folder_path):
        os.mkdir(date_folder_path)

    sneakers_downloaded: int = 0
    for sneaker in sneakers:
        success = download_image(folder=date_folder_path, url=sneaker["image"])
        sneakers_downloaded += success
    return sneakers_downloaded


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


def message(text: str, is_input: bool = False, extra: Any = "default") -> Optional[str]:
    return input(Color(text, extra)) if is_input else print(Color(text, extra))
