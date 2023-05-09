import scrapy
from jobscrapper.items import OfferItem

class JobspiderSpider(scrapy.Spider):
    name = "jobspider"
    allowed_domains = ["www.hellowork.com"]
    start_urls = ["https://www.hellowork.com/fr-fr/stage/domaine_informatique.html"]

    i = 2
    def parse(self, response):
        offers = response.xpath("//li[contains(@class, '!tw-mb-6')]")
        for offer in offers:
            next_offer = offer.xpath("./div/@id").get()

            if next_offer is not None:
                next_offer_url = f'https://www.hellowork.com/fr-fr/emplois/{next_offer}.html'
                yield response.follow(next_offer_url, callback=self.parse_offer_page)

        next_page = response.css('span.atc.next').get()
        if next_page is not None:
            print('***************************************')
            print(JobspiderSpider.i)
            next_page_url = f'https://www.hellowork.com/fr-fr/stage/domaine_informatique.html?p={JobspiderSpider.i}'
            JobspiderSpider.i += 1
            yield response.follow(next_page_url, callback=self.parse)

    def parse_offer_page(self, response):
        offer_item = OfferItem()

        offer_item['url'] = response.url.strip(),
        offer_item['title'] = response.css('h1 span ::text').get().strip(),
        offer_item['company'] = response.css('h1::text').get().strip(),
        offer_item['description'] = ' '.join([desc.strip() for sublist in response.css('p.tw-typo-long-m') for desc in sublist.css('::text').getall()]),
        offer_item['city'] = response.xpath("//h1/following-sibling::ul//li/span/text()").getall()[1].strip(),
        offer_item['offer_type'] = response.xpath("//h1/following-sibling::ul//li/span/text()").getall()[3].strip(),
        offer_item['tags'] = [tag.strip() for tag in response.css('li.tag-offer.single::text').getall()],

        yield offer_item
