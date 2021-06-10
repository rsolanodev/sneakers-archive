import json
from typing import Dict, List

import requests
from bs4 import BeautifulSoup

from sneakers.exceptions import BrandDoesNotExist
from sneakers.helpers import download_images


class SneakerScraper:
    BASE_URL: str = "https://solecollector.com"

    def __init__(self):
        self.brands: Dict[str, str] = self.scrap_brands()
        self.sneakers: List = []

    def parse_url(self, url) -> str:
        return self.BASE_URL + url

    def scrap_brands(self) -> Dict:
        """Gets the names of the brands and their links"""
        response = requests.get(self.parse_url("/sd/sole-search-sneaker-database/"))
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.find_all("div", class_="brand-banner brand-item")
        brands: Dict[str, str] = {}
        for brand in items:
            name: str = brand.find("img")["alt"]
            brands[name] = brand.find("a")["href"]
        return brands

    def get_sneakers(
        self, brand_id: str, get: int = 100, skip: int = 0
    ) -> requests.Response:
        """
        :param brand_id: brand identifier
        :param get: quantity of items to obtain
        :param skip: items to skip
        """
        api_url = self.parse_url("/api/sneaker-api/releases?")
        url = f"{api_url}asc=0&get={get}&parent_id={brand_id}&skip={skip}&start=1623258117.75"
        return requests.get(url)

    @staticmethod
    def get_brand_id(url: str) -> str:
        """The brand id is obtained from the url."""
        return url.split("/")[-3]

    def add_sneaker(self, sneaker: Dict) -> None:
        self.sneakers.append(
            {
                "name": sneaker["name"],
                "image": sneaker["hero_image_url"],
                "date": sneaker["release_date"],
            }
        )

    def scrap_sneakers(self, name: str, start: int = 0, limit: int = 0) -> List:
        """
        :param name: brand name
        :param start: number to start getting data on
        :param limit: number of desired sneakers
        """
        if name in self.brands:
            brand_url = self.brands[name]
            brand_id = self.get_brand_id(brand_url)
            is_ok, data, skip = True, True, start

            while (
                is_ok and data and (limit and len(self.sneakers) < limit) or not limit
            ):
                response = self.get_sneakers(brand_id=brand_id, skip=skip)
                is_ok, data = response.ok, json.loads(response.text)
                if is_ok:
                    for sneaker in data:
                        if (limit and len(self.sneakers) < limit) or not limit:
                            self.add_sneaker(sneaker=sneaker)
                skip += 100
            download_images(brand=name, sneakers=self.sneakers)
        else:
            raise BrandDoesNotExist(
                "The specified brand name does not exist, please try Nike, Adidas, Reebok, "
                "Puma, Jordan, Converse, Vans, New Balance or ASICS."
            )
        return self.sneakers
