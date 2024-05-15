import scrapy
from scrapy.crawler import CrawlerProcess

head = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

class Scholarship_Web_Spider(scrapy.Spider):
    name = "scholarship_web_spider"

    def start_requests(self):
        yield scrapy.Request(url="https://www.polyu.edu.hk/sao/student-resources-and-support-section/scholarships/scholarship-types/",
                             callback=self.parse, headers=head)

    def parse(self, response):
        html_content = response.css("main.page-content").getall()
        filepath = 'scholarship_info.html'
        with open(filepath, 'w') as f:
            f.write(html_content[0])

class Scholarship_Link_Spider(scrapy.Spider):
    name = "scholarship_link_spider"

    def start_requests(self):
        yield scrapy.Request(url="https://www.polyu.edu.hk/sao/student-resources-and-support-section/scholarships/scholarship-types/",
                             callback=self.parse, headers=head)

    def parse(self, response):
        # Get all the picture links inside <main class="page-content">
        picture_links = response.css("main.page-content a::attr(href)").getall()
        filepath = 'scholarship_links.txt'
        with open(filepath, 'w') as f:
            f.write("Here are some useful links for scholarships:\n")
            for link in picture_links:
                # Delete if the link begins with "#!"
                if link.startswith("#!"):
                    continue
                if link.startswith("/"):
                    link = "https://www.polyu.edu.hk" + link
                f.write(link + "\n")

process = CrawlerProcess()
process.crawl(Scholarship_Web_Spider)
#process.crawl(Scholarship_Link_Spider)
process.start()