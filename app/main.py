import os
from typing import Optional
import sys
import sqlite3
import multiprocessing
from fastapi import FastAPI
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

sys.path.append(os.path.join(os.getcwd()))

app = FastAPI(title="BMW Scraper API", version="1.0.0")

DB_PATH = "bmw_cars.db"


def run_spider():
    try:
        from app.spiders.bmw import BmwSpider

        os.environ.setdefault("SCRAPY_SETTINGS_MODULE", "app.settings")
        settings = get_project_settings()
        process = CrawlerProcess(settings)
        process.crawl(BmwSpider)
        process.start()
    except Exception as e:
        print(f"Error starting spider: {e}")


@app.post("/run-scraping", tags=["Control"])
async def trigger_scraping():
    p = multiprocessing.Process(target=run_spider)
    p.start()
    return {"message": "Scraping started", "status": "running"}


@app.get("/cars", tags=["Data"])
async def get_scraped_cars(
    model: Optional[str] = None,
    fuel: Optional[str] = None,
    transmission: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    limit: int = 100,
    offset: int = 0,
):
    if not os.path.exists(DB_PATH):
        return {"error": "Database not found. Please run scraping first."}

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM cars WHERE 1=1"
    params = []

    if model:
        query += " AND model LIKE ?"
        params.append(f"%{model}%")
    if fuel:
        query += " AND fuel = ?"
        params.append(fuel)
    if transmission:
        query += " AND transmission = ?"
        params.append(transmission)
    if min_price is not None:
        query += " AND price >= ?"
        params.append(min_price)
    if max_price is not None:
        query += " AND price <= ?"
        params.append(max_price)

    query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


@app.get("/health", tags=["System"])
async def health():
    return {"status": "ok"}
