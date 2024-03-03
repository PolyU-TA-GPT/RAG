import scrapy
from scrapy.crawler import CrawlerProcess

head = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

class Srs_Web_Spider(scrapy.Spider):
    name = "srs_web_spider"

    def start_requests(self):
        yield scrapy.Request(url="https://www.polyu.edu.hk/sao/student-resources-and-support-section/residential-life/hall-admission/admission-policies-undergraduates/special-readmission-scheme-srs/",
                             callback=self.parse, headers=head)

    def parse(self, response):
        # Get all the pure text inside <div class="container static-content color-set--red">
        text = response.css("div.container.static-content.color-set--red ::text").getall()
        pure_text = ' '.join(text).strip()
        pure_text = pure_text.replace('\n', ' ').replace('  ', ' ')
        filepath = 'srs_info.txt'
        with open(filepath, 'w') as f:
            f.write(pure_text)


class Srs_Link_Spider(scrapy.Spider):
    name = "srs_link_spider"

    def start_requests(self):
        yield scrapy.Request(url="https://www.polyu.edu.hk/sao/student-resources-and-support-section/residential-life/hall-admission/admission-policies-undergraduates/special-readmission-scheme-srs/",
                             callback=self.parse, headers=head)

    def parse(self, response):
        # Get all the picture links inside <div class="container static-content color-set--red">
        picture_links = response.css("div.container.static-content.color-set--red a::attr(href)").getall()
        filepath = 'srs_links.txt'
        with open(filepath, 'w') as f:
            f.write("Here are some useful links for SRS:\n")
            for link in picture_links:
                # Delete if the link begins with "#!"
                if link.startswith("#!"):
                    continue
                if link.startswith("/"):
                    link = "https://www.polyu.edu.hk" + link
                f.write(link + "\n")

process = CrawlerProcess()
# process.crawl(Srs_Web_Spider)
# process.crawl(Srs_Link_Spider)
process.start()