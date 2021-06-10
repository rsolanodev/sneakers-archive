from unittest import mock

from sneakers.constants import ADIDAS
from sneakers.exceptions import BrandDoesNotExist
from sneakers.scrapers import SneakerScraper
from tests.mocks import download_images

SOLE_COLLECTOR_BRANDS = 9


def test_brands_length():
    scraper = SneakerScraper()
    assert len(scraper.brands) == SOLE_COLLECTOR_BRANDS


@mock.patch("sneakers.scrapers.download_images", download_images)
def test_scrap_sneakers():
    scraper, limit = SneakerScraper(), 10
    sneakers = scraper.scrap_sneakers(name=ADIDAS, limit=limit)
    assert len(sneakers) == limit


@mock.patch("sneakers.scrapers.download_images", download_images)
def test_scrap_sneakers_with_unavailable_brand():
    scraper = SneakerScraper()
    try:
        scraper.scrap_sneakers(name="Racks")
        exception = False
    except BrandDoesNotExist:
        exception = True
    assert exception
