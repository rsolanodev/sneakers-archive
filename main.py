from datetime import datetime

import enquiries

from sneakers.constants import Brand
from sneakers.exceptions import BrandDoesNotExist
from sneakers.helpers import message
from sneakers.scrapers import SneakerScraper

IMAGES_BY_BRAND = "Get images by brand"
IMAGES_BY_DATES = "Get images by dates"

scraper = SneakerScraper()


def get_images_by_brand():
    brands = Brand.all()
    brand = enquiries.choose("Select brand: ", brands)
    try:
        start = message("Image list start number [0]: ", True) or "0"
        while not start.isnumeric():
            start = message("Image list start number [0]: ", True) or "0"
        limit = message("Amount of images [100]: ", True) or "100"
        while not limit.isnumeric():
            limit = message("Amount of images [100]: ", True) or "100"
        message("\nThe images will start to download, please be patient!")
        sneakers = scraper.scrap_sneakers_by_brand(
            name=brand, start=int(start), limit=int(limit)
        )
        if sneakers:
            message(f"\n{sneakers} images have been generated! 😁")
        else:
            message(
                "\nNo sneakers found or you already have them downloaded! 😔️",
                extra="warning",
            )
    except BrandDoesNotExist:
        message(
            "\nThe chosen brand was not found, our administrators will solve it soon!",
            extra="danger",
        )
        message("Please select a different brand")
        get_images_by_brand()


def get_images_by_dates():
    after = message("Date from (dd/mm/yyyy): ", True)
    while not after:
        after = message("Date from (dd/mm/yyyy): ", True, "mandatory")
    today = datetime.today().strftime("%d/%m/%Y")
    before = message(f"Date to (dd/mm/yyyy) [{today}]: ", True)
    try:
        after_date = datetime.strptime(after, "%d/%m/%Y")
        before_date = (
            datetime.strptime(before, "%d/%m/%Y") if before else datetime.today()
        )
        message("\nThe images will start to download, please be patient!")
        sneakers = scraper.scrap_sneakers_by_dates(after_date, before_date)
        if sneakers:
            message(f"\n{sneakers} images have been generated! 😁")
        else:
            message(
                "\nNo sneakers found or you already have them downloaded! 😔️",
                extra="warning",
            )
    except ValueError:
        message("\nDates not readable, enter a correct format", extra="danger")
        get_images_by_dates()


if __name__ == "__main__":
    options = [IMAGES_BY_BRAND, IMAGES_BY_DATES]
    choice = enquiries.choose("How do you want to get the images: ", options)

    if choice == IMAGES_BY_BRAND:
        get_images_by_brand()
    else:
        get_images_by_dates()
