from datetime import datetime
from unittest import mock

from sneakers.constants import Brand
from sneakers.exceptions import BrandDoesNotExist
from sneakers.scrapers import SneakerScraper
from tests.mocks import download_images_by_brand, download_images_by_date

SOLE_COLLECTOR_BRANDS = 9
ALL_SNEAKERS_IN_2020_09 = 53


def test_brands_length():
    scraper = SneakerScraper()
    assert len(scraper.brands) == SOLE_COLLECTOR_BRANDS


@mock.patch("sneakers.scrapers.download_images_by_brand", download_images_by_brand)
def test_scrap_sneakers_by_brand():
    scraper, limit = SneakerScraper(), 10
    scraper.scrap_sneakers_by_brand(name=Brand.ADIDAS, limit=limit)
    assert scraper.sneakers_downloaded == limit


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
    date = datetime(2020, 9, 1)
    scraper.scrap_sneakers_by_dates(after_date=date, before_date=date)
    assert scraper.sneakers_downloaded == ALL_SNEAKERS_IN_2020_09
