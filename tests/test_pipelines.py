import pytest
import sqlite3
from unittest.mock import patch
from scrapy.exceptions import DropItem
from scrapy.spiders import Spider
from scrapy.crawler import Crawler
from app.pipelines import ValidationAndCleaningPipeline, SQLitePipeline
from app.items import BmwCarItem
from itemadapter import ItemAdapter


@pytest.fixture
def clean_db_path(tmp_path):
    return str(tmp_path / "pipeline_clean_test.db")


def create_test_item(registration="AA1111", model="X5"):
    item = BmwCarItem()
    adapter = ItemAdapter(item)
    adapter["registration"] = registration
    adapter["model"] = model
    adapter["name"] = "BMW X5"
    adapter["mileage"] = "1000"
    adapter["registered"] = "2024"
    adapter["engine"] = "3.0"
    adapter["range"] = "None"
    adapter["exterior"] = "White"
    adapter["fuel"] = "Petrol"
    adapter["transmission"] = "Auto"
    adapter["upholstery"] = "Leather"
    return item


def test_validation_pipeline_success():
    pipeline = ValidationAndCleaningPipeline()
    spider = Spider(name="test")
    item = create_test_item(registration="AA1111")
    processed = pipeline.process_item(item, spider)
    assert ItemAdapter(processed).get("registration") == "AA1111"


def test_validation_pipeline_drop():
    pipeline = ValidationAndCleaningPipeline()
    spider = Spider(name="test")
    item = create_test_item(registration=None)
    with pytest.raises(DropItem):
        pipeline.process_item(item, spider)


def test_pipelines_from_crawler():
    crawler = Crawler(Spider)
    if hasattr(ValidationAndCleaningPipeline, "from_crawler"):
        assert ValidationAndCleaningPipeline.from_crawler(crawler) is not None
    if hasattr(SQLitePipeline, "from_crawler"):
        assert SQLitePipeline.from_crawler(crawler) is not None


def test_sqlite_pipeline(clean_db_path):
    spider = Spider(name="test")
    pipeline = SQLitePipeline()

    real_connect = sqlite3.connect

    def mock_connect(*args, **kwargs):
        return real_connect(clean_db_path)

    with patch("app.pipelines.sqlite3.connect", side_effect=mock_connect):
        pipeline.open_spider(spider)
        item = create_test_item(registration="NEW_TEST_123")
        pipeline.process_item(item, spider)
        pipeline.close_spider(spider)

    # Перевіряємо в чистій базі
    conn = real_connect(clean_db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars WHERE registration='NEW_TEST_123'")
    assert cursor.fetchone() is not None
    conn.close()


def test_sqlite_pipeline_duplicate_insert(clean_db_path):
    spider = Spider(name="test")
    pipeline = SQLitePipeline()

    real_connect = sqlite3.connect

    def mock_connect(*args, **kwargs):
        return real_connect(clean_db_path)

    with patch("app.pipelines.sqlite3.connect", side_effect=mock_connect):
        pipeline.open_spider(spider)
        item = create_test_item(registration="DUPLICATE_123")

        pipeline.process_item(item, spider)

        try:
            pipeline.process_item(item, spider)
        except Exception:
            pass

        pipeline.close_spider(spider)

    conn = real_connect(clean_db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM cars WHERE registration='DUPLICATE_123'")
    assert cursor.fetchone()[0] == 1
    conn.close()
