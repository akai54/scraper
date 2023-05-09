import scrapy


class JobscrapperItem(scrapy.Item):
    name = scrapy.Field()
    pass

class OfferItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    company = scrapy.Field()
    description = scrapy.Field()
    city = scrapy.Field()
    offer_type = scrapy.Field()
    tags = scrapy.Field()
