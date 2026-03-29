from unittest.mock import patch
from app.main import run_spider


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_cars_success(client):
    response = client.get("/cars")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_cars_filtering(client):
    response = client.get("/cars?model=X5&min_price=50000")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["model"] == "X5"


def test_get_cars_no_db(client):
    with patch("app.main.os.path.exists", return_value=False):
        response = client.get("/cars")
        assert response.status_code == 200
        assert "error" in response.json()


def test_trigger_scraping(client):
    with patch("app.main.multiprocessing.Process") as mock_process:
        response = client.post("/run-scraping")
        assert response.status_code == 200
        mock_process.return_value.start.assert_called_once()


def test_run_spider_success():
    with patch("app.main.CrawlerProcess") as mock_process:
        run_spider()
        mock_process.assert_called_once()
        mock_process.return_value.start.assert_called_once()


def test_run_spider_exception(capsys):
    with patch("app.main.CrawlerProcess", side_effect=Exception("Test Exception")):
        run_spider()
        captured = capsys.readouterr()
        assert "Error starting spider: Test Exception" in captured.out


def test_get_cars_all_filters_and_pagination(client):
    response = client.get(
        "/cars?fuel=Petrol&transmission=Manual&max_price=30000&limit=1&offset=0"
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["model"] == "3 Series"
    assert data[0]["fuel"] == "Petrol"
    assert data[0]["transmission"] == "Manual"
