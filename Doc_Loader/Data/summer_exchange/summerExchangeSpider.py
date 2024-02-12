import scrapy
from scrapy.crawler import CrawlerProcess

head = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# website text spider
class Summer_Exchange_Web_Spider(scrapy.Spider):
    name = "summer_exchange_spider"

    def start_requests(self):
        yield scrapy.Request(url="https://www.polyu.edu.hk/geo/exchange-and-study-abroad/outgoing-students/summer-exchange/",
                             callback=self.parse, headers=head)

    def parse(self, response):
        # Get all the pure text inside <main class="page-content">
        text = response.css("main.page-content ::text").getall()
        pure_text = ' '.join(text).strip()
        pure_text = pure_text.replace('\n', ' ').replace('  ', ' ')
        filepath = 'summer_exchange_info.txt'
        with open(filepath, 'w') as f:
            f.write(pure_text)

class Summer_Exchange_Link_Spider(scrapy.Spider):
    name = "summer_exchange_link_spider"

    def start_requests(self):
        yield scrapy.Request(url="https://www.polyu.edu.hk/geo/exchange-and-study-abroad/outgoing-students/summer-exchange/",
                             callback=self.parse, headers=head)

    def parse(self, response):
        # Get all the picture links inside <main class="page-content">
        picture_links = response.css("main.page-content a::attr(href)").getall()
        filepath = 'summer_exchange_links.txt'
        with open(filepath, 'w') as f:
            f.write("Here are some useful links for summer exchange:\n")
            for link in picture_links:
                # Delete if the link begins with "#!"
                if link.startswith("#!"):
                    continue
                if link.startswith("/"):
                    link = "https://www.polyu.edu.hk" + link
                f.write(link + "\n")

class Summer_OxBridge_Web_Spider(scrapy.Spider):
    name = "summer_oxbridge_web_spider"

    def start_requests(self):
        yield scrapy.Request(url="https://www.polyu.edu.hk/geo/exchange-and-study-abroad/outgoing-students/summer-oxbridge/",
                             callback=self.parse, headers=head)

    def parse(self, response):
        # Get all the pure text inside <main class="page-content">
        text = response.css("main.page-content ::text").getall()
        pure_text = ' '.join(text).strip()
        pure_text = pure_text.replace('\n', ' ').replace('  ', ' ')
        filepath = 'summer_oxbridge_info.txt'
        with open(filepath, 'w') as f:
            f.write(pure_text)

class Summer_Oxbridge_Link_Spider(scrapy.Spider):
    name = "summer_oxbridge_link_spider"

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.polyu.edu.hk/geo/exchange-and-study-abroad/outgoing-students/summer-oxbridge/",
            callback=self.parse, headers=head)

    def parse(self, response):
        picture_links = response.css("main.page-content a::attr(href)").getall()
        filepath = 'summer_oxbridge_links.txt'
        with open(filepath, 'w') as f:
            f.write("Here are some useful links for summer oxbridge:\n")
            for link in picture_links:
                # Delete if the link begins with "#!"
                if link.startswith("#!"):
                    continue
                if link.startswith("/"):
                    link = "https://www.polyu.edu.hk" + link
                f.write(link + "\n")


process = CrawlerProcess()
# process.crawl(Summer_Exchange_Web_Spider)
# process.crawl(Summer_Exchange_Link_Spider)
# process.crawl(Summer_OxBridge_Web_Spider)
# process.crawl(Summer_Oxbridge_Link_Spider)

process.start()