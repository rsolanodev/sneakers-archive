from unittest import mock

from sneakers.constants import ADIDAS
from sneakers.exceptions import BrandDoesNotExist
from sneakers.scrapers import SneakerScraper
from tests.mocks import download_images_by_brand, download_images_by_date

SOLE_COLLECTOR_BRANDS = 9
ALL_SNEAKERS_IN_2020_03 = 22


def test_brands_length():
    scraper = SneakerScraper()
    assert len(scraper.brands) == SOLE_COLLECTOR_BRANDS


@mock.patch("sneakers.scrapers.download_images_by_brand", download_images_by_brand)
def test_scrap_sneakers_by_brand():
    scraper, limit = SneakerScraper(), 10
    sneakers = scraper.scrap_sneakers_by_brand(name=ADIDAS, limit=limit)
    assert len(sneakers) == limit


@mock.patch("sneakers.scrapers.download_images_by_brand", download_images_by_brand)
def test_scrap_sneakers_by_brand_with_unavailable_brand():
    scraper = SneakerScraper()
    try:
        scraper.scrap_sneakers_by_brand(name="Racks")
        exception = False
    except BrandDoesNotExist:
        exception = True
    assert exception


@mock.patch("sneakers.scrapers.download_images_by_date", download_images_by_date)
def test_scrap_sneakers_by_dates():
    scraper = SneakerScraper()
    sneakers = scraper.scrap_sneakers_by_dates(after="01/03/2020", before="01/03/2020")
    assert len(sneakers) == ALL_SNEAKERS_IN_2020_03
