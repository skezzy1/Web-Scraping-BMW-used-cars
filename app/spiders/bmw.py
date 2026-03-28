import scrapy
import json
import re
from scrapy_playwright.page import PageMethod
from app.loaders import BmwItemLoader
from app.items import BmwCarItem

class BmwSpider(scrapy.Spider):
    name = "bmw"
    allowed_domains = ["usedcars.bmw.co.uk"]

    custom_settings = {
        'DOWNLOAD_HANDLERS': {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        'TWISTED_REACTOR': "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        'PLAYWRIGHT_BROWSER_TYPE': 'chromium',
        'PLAYWRIGHT_LAUNCH_OPTIONS': {
            'headless': True,
        },
        'CONCURRENT_REQUESTS': 16,
        'PLAYWRIGHT_MAX_PAGES_PER_CONTEXT': 4,

        'DOWNLOADER_MIDDLEWARES': {
            'app.middlewares.RandomUserAgentMiddleware': 400,
        },
        'ITEM_PIPELINES': {
            'app.pipelines.ValidationAndCleaningPipeline': 100,
            'app.pipelines.SQLitePipeline': 200,
        },
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 1.0,
        'COOKIES_ENABLED': True,
    }

    def start_requests(self):
        self.logger.info("Starting parsing for 5 pages")
        for page in range(1, 6):
            url = f"https://usedcars.bmw.co.uk/result/?payment_type=cash&size=23&source=home&page={page}"
            yield scrapy.Request(
                url,
                callback=self.parse_result_page,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_load_state", "networkidle")
                    ]
                },
                dont_filter=True
            )

    def parse_result_page(self, response):
        car_links = response.xpath('//a[contains(@href, "/vehicle/")]/@href').getall()
        if not car_links:
            return

        for link in set(car_links):
            yield response.follow(
                link,
                callback=self.parse_detail_page,
                meta={"playwright": True}
            )

    def parse_detail_page(self, response):
        script_text = response.xpath('//script[contains(text(), "UVL.AD =")]/text()').get()
        if not script_text:
            return

        json_match = re.search(r'UVL\.AD\s*=\s*({.*?});\s*UVL\.AOS_PLAYER', script_text, re.DOTALL)
        if not json_match:
            return

        try:
            car_data = json.loads(json_match.group(1))
        except json.JSONDecodeError:
            return

        loader = BmwItemLoader(item=BmwCarItem(), response=response)
        loader.add_value('model', car_data.get('title'))
        loader.add_value('name', car_data.get('sale_title'))
        loader.add_value('registration', car_data.get('identification', {}).get('registration'))

        mileage = car_data.get('condition_and_state', {}).get('mileage')
        loader.add_value('mileage', str(mileage) if mileage is not None else None)

        loader.add_value('registered', car_data.get('dates', {}).get('registration'))

        engine_litres = car_data.get('engine', {}).get('size', {}).get('litres')
        loader.add_value('engine', str(engine_litres) if engine_litres else None)

        battery_range = car_data.get('battery', {}).get('range', {}).get('value')
        loader.add_value('range', str(battery_range) if battery_range else None)

        loader.add_value('exterior', car_data.get('colour', {}).get('manufacturer_colour'))

        spec = car_data.get('specification', {})
        loader.add_value('fuel', spec.get('raw_fuel_type'))
        loader.add_value('transmission', spec.get('transmission'))
        loader.add_value('upholstery', spec.get('interior'))

        yield loader.load_item()