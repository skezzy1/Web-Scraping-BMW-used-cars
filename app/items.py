import scrapy
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class BmwCarItem:
    model: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    registration: Optional[str] = field(default=None)
    mileage: Optional[int] = field(default=None)
    registered: Optional[str] = field(default=None)
    engine: Optional[str] = field(default=None)
    range: Optional[str] = field(default=None)
    exterior: Optional[str] = field(default=None)
    fuel: Optional[str] = field(default=None)
    transmission: Optional[str] = field(default=None)
    upholstery: Optional[str] = field(default=None)


# class BMWCarItem(scrapy.Item):
#     model = scrapy.Field()
#     name = scrapy.Field()
#     registration = scrapy.Field()
#     mileage = scrapy.Field()
#     registered = scrapy.Field()
#     engine = scrapy.Field()
#     range = scrapy.Field()
#     exterior = scrapy.Field()
#     fuel = scrapy.Field()
#     transmission = scrapy.Field()
#     upholstery = scrapy.Field()
#

