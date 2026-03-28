import sqlite3
import logging
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter

logger = logging.getLogger(__name__)


class ValidationAndCleaningPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if (
            not adapter.get("model")
            or not adapter.get("name")
            or not adapter.get("registration")
        ):
            logger.warning(
                f"Dropping item: missing required fields. Registration: {adapter.get('registration')}"
            )
            raise DropItem(f"Missing required field in {item}")

        if adapter.get("mileage"):
            try:
                clean_mileage = (
                    str(adapter["mileage"]).replace(",", "").replace(" ", "").strip()
                )
                adapter["mileage"] = int(clean_mileage)
            except ValueError:
                logger.warning(f"Could not convert mileage: {adapter['mileage']}")
                adapter["mileage"] = None

        if adapter.get("fuel"):
            adapter["fuel"] = adapter["fuel"].lower()

        return item


class SQLitePipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect("bmw_cars.db")
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cars (
                registration TEXT PRIMARY KEY,
                model TEXT NOT NULL,
                name TEXT NOT NULL,
                mileage INTEGER,
                registered TEXT,
                engine TEXT,
                range TEXT,
                exterior TEXT,
                fuel TEXT,
                transmission TEXT,
                upholstery TEXT
            )
        """)
        self.connection.commit()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        data = adapter.asdict()

        try:
            self.cursor.execute(
                """
                INSERT OR IGNORE INTO cars (
                    registration, model, name, mileage, registered, engine, 
                    range, exterior, fuel, transmission, upholstery
                ) VALUES (
                    :registration, :model, :name, :mileage, :registered, :engine, 
                    :range, :exterior, :fuel, :transmission, :upholstery
                )
            """,
                data,
            )
            self.connection.commit()
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")

        return item

    def close_spider(self, spider):
        if hasattr(self, "connection"):
            self.connection.close()
