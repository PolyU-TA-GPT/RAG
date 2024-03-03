import scrapy
from scrapy.crawler import CrawlerProcess

head = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

class New_Car_Text_Spider(scrapy.Spider):
    name = "new_car_text_spider"

    def start_requests(self):
        yield scrapy.Request(url="https://www.polyu.edu.hk/ous/GURSubjects/CAR.php",
                             callback=self.parse, headers=head)

    def parse(self, response):
        # Get the pure text inside <div class="container static-content color-set--red">
        text = response.css("div.container.static-content.color-set--red ::text").getall()
        pure_text = ' '.join(text).strip()
        pure_text = pure_text.replace('\n', ' ').replace('  ', ' ')
        filepath = 'new_car_info.txt'
        with open(filepath, 'w') as f:
            f.write(pure_text)
        text2 = response.css("table.static-table--less-padding-fullWidth--border--zebra ::text").getall()
        pure_text2 = ' '.join(text2).strip()
        pure_text2 = pure_text2.replace('\n', ' ').replace('  ', ' ')
        with open(filepath, 'a') as f:
            f.write(pure_text2)

class New_Car_Link_Spider(scrapy.Spider):
    name = "new_car_link_spider"

    def start_requests(self):
        yield scrapy.Request(url="https://www.polyu.edu.hk/ous/GURSubjects/CAR.php",
                             callback=self.parse, headers=head)

    def parse(self, response):
        # Get all the links inside <table class="static-table--less-padding-fullWidth--border--zebra">
        links = response.css("table.static-table--less-padding-fullWidth--border--zebra a::attr(href)").getall()
        filepath = 'new_car_links.txt'
        with open(filepath, 'w') as f:
            f.write("Here are some useful links for new CAR courses:\n")
            for link in links:
                if link.startswith("#!"):
                    continue
                if link.startswith("/"):
                    link = "https://www.polyu.edu.hk" + link
                f.write(link + "\n")

class Old_Car_Text_Spider(scrapy.Spider):
    name = "old_car_text_spider"

    def start_requests(self):
        yield scrapy.Request(url="https://www.polyu.edu.hk/ous/GURSubjects/CAR_2021.php",
                             callback=self.parse, headers=head)

    def parse(self, response):
        # Get the pure text inside <div class="container static-content color-set--red">
        text = response.css("div.container.static-content.color-set--red ::text").getall()
        pure_text = ' '.join(text).strip()
        pure_text = pure_text.replace('\n', ' ').replace('  ', ' ')
        filepath = 'old_car_info.txt'
        with open(filepath, 'w') as f:
            f.write(pure_text)
        text2 = response.css("table.static-table--less-padding-fullWidth--border--zebra ::text").getall()
        pure_text2 = ' '.join(text2).strip()
        pure_text2 = pure_text2.replace('\n', ' ').replace('  ', ' ')
        with open(filepath, 'a') as f:
            f.write(pure_text2)

class Old_Car_Link_Spider(scrapy.Spider):
    name = "old_car_link_spider"

    def start_requests(self):
        yield scrapy.Request(url="https://www.polyu.edu.hk/ous/GURSubjects/CAR_2021.php",
                             callback=self.parse, headers=head)

    def parse(self, response):
        # Get all the links inside <table class="static-table--less-padding-fullWidth--border--zebra">
        links = response.css("table.static-table--less-padding-fullWidth--border--zebra a::attr(href)").getall()
        filepath = 'old_car_links.txt'
        with open(filepath, 'w') as f:
            f.write("Here are some useful links for old CAR courses:\n")
            for link in links:
                if link.startswith("#!"):
                    continue
                if link.startswith("/"):
                    link = "https://www.polyu.edu.hk" + link
                f.write(link + "\n")


process = CrawlerProcess()
# process.crawl(New_Car_Text_Spider)
# process.crawl(New_Car_Link_Spider)
# process.crawl(Old_Car_Text_Spider)
# process.crawl(Old_Car_Link_Spider)
process.start()