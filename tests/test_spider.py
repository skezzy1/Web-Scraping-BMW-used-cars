from scrapy.http import HtmlResponse
from app.spiders.bmw import BmwSpider


def test_start_requests():
    spider = BmwSpider()
    requests = list(spider.start_requests())
    assert len(requests) == 5
    assert "page=1" in requests[0].url


def test_parse_result_page_success():
    spider = BmwSpider()
    mock_html = b'<html><a href="/vehicle/123">Link 1</a><a href="/vehicle/456">Link 2</a></html>'
    response = HtmlResponse(url="https://fake.com", body=mock_html, encoding="utf-8")
    yields = list(spider.parse_result_page(response))
    assert len(yields) == 2


def test_parse_result_page_empty():
    spider = BmwSpider()
    mock_html = b"<html><body>No links here</body></html>"
    response = HtmlResponse(url="https://fake.com", body=mock_html, encoding="utf-8")
    assert list(spider.parse_result_page(response)) == []


def test_parse_detail_page_no_script():
    spider = BmwSpider()
    mock_html = b"<html><body>No script</body></html>"
    response = HtmlResponse(url="https://fake.com", body=mock_html, encoding="utf-8")
    assert list(spider.parse_detail_page(response)) == []


def test_parse_detail_page_no_json_match():
    spider = BmwSpider()
    mock_html = b'<script>UVL.AD = "not a json object";</script>'
    response = HtmlResponse(url="https://fake.com", body=mock_html, encoding="utf-8")
    assert list(spider.parse_detail_page(response)) == []


def test_parse_detail_page_bad_json():
    spider = BmwSpider()
    mock_html = b"<script>UVL.AD = {bad_json:,,}; UVL.AOS_PLAYER</script>"
    response = HtmlResponse(url="https://fake.com", body=mock_html, encoding="utf-8")
    assert list(spider.parse_detail_page(response)) == []


def test_parse_detail_page_success():
    spider = BmwSpider()
    mock_html = b"""
    <script>
    UVL.AD = {
        "title": "X5",
        "sale_title": "BMW X5",
        "identification": {"registration": "AA1234"},
        "condition_and_state": {"mileage": 1000},
        "dates": {"registration": "2020"},
        "engine": {"size": {"litres": 3.0}},
        "battery": {"range": {"value": 50}},
        "colour": {"manufacturer_colour": "Black"},
        "specification": {"raw_fuel_type": "Diesel", "transmission": "Auto", "interior": "Leather"}
    };
    UVL.AOS_PLAYER = true;
    </script>
    """
    response = HtmlResponse(url="https://fake.com", body=mock_html, encoding="utf-8")
    items = list(spider.parse_detail_page(response))
    assert len(items) == 1
    assert items[0] is not None
