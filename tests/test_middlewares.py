from app.middlewares import RandomUserAgentMiddleware
from scrapy.http import Request
from scrapy.spiders import Spider


def test_random_user_agent_middleware():
    spider = Spider(name="test")
    middleware = RandomUserAgentMiddleware()

    request = Request(url="https://test.com")
    middleware.process_request(request, spider)

    assert b"User-Agent" in request.headers
