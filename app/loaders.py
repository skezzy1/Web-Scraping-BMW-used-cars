from itemloaders import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose


class BmwItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(str.strip)
