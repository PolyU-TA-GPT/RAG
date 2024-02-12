# import scrapy
import scrapy
from scrapy.crawler import CrawlerProcess

head = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

# FB (Af, MM, LMS)
class AF_Course_Spider(scrapy.Spider):
    name = "af_course_spider"

    def start_requests(self):
        base_url = "https://www.polyu.edu.hk/af/study/subject-syllabi/?category=Undergraduate&keyword="
        pages = range(1, 6)  # Pages 1 to 5
        urls = [base_url + "&page=" + str(page) for page in pages]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=head)

    def parse(self, response):
        tr_elements = response.css('table.static-table--less-padding-fullWidth--border-default--zebra > tr[data-href]')
        for tr in tr_elements:
            course_text = tr.attrib['data-href']
            filepath = 'af_course_info.txt'
            course_link = "https://www.polyu.edu.hk" + course_text
            with open(filepath, 'a') as f:
                f.write(course_link + "\n")

class MM_Course_Spider(scrapy.Spider):
    name = "mm_course_spider"

    def start_requests(self):
        # craw multiple urls here
        yield scrapy.Request(url="https://www.polyu.edu.hk/mm/study/subject-syllabi//",
                             callback=self.parse, headers=head)

    def parse(self, response):
        course_container = response.css('div.border-blk-tab__tab-pane.active')
        course_table = course_container.css('table.white-style')
        course_texts = course_table.css('a::attr(href)').extract()
        filepath = 'mm_course_info.txt'
        for course_text in course_texts:
            course_link = "https://www.polyu.edu.hk" + course_text
            with open(filepath, 'a') as f:
                f.write(course_link + "\n")

class  LMS_Course_Spider(scrapy.Spider):
    name = "lms_course_spider"

    def start_requests(self):
        # craw multiple urls here
        base_url = "https://www.polyu.edu.hk/lms/study/subject-syllabi/?category=Undergraduate%20Subjects&keyword=&page="
        pages = range(1, 7)  # Pages 1 to 6
        urls = [base_url + str(page) for page in pages]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=head)

    def parse(self, response):
        tr_elements = response.css('table.static-table--less-padding-fullWidth--border-default--zebra > tr[data-href]')
        for tr in tr_elements:
            course_text = tr.attrib['data-href']
            filepath = 'lms_course_info.txt'
            with open(filepath, 'a') as f:
                f.write(course_text + "\n")

# FCE (BRE, BEEE, CEE, LSGI)
class BRE_Course_Spider(scrapy.Spider):
    name = "bre_course_spider"

    def start_requests(self):
        # craw multiple urls here
        yield scrapy.Request(url="https://www.polyu.edu.hk/en/bre/study/undergraduate-programmes/subjects_syllabi/2023-2024/", callback=self.parse,
                             headers=head)

    def parse(self, response):
        course_container = response.css('table.static-table--normal--border-default--no-zebra ')
        course_links = course_container.css('a::attr(href)').extract()
        filepath = 'bre_course_info.txt'
        with open(filepath, 'w') as f:
            f.writelines(["https://www.polyu.edu.hk" + c + "\n" for c in course_links])

# class BEEE_Course_Spider(scrapy.Spider):

class CEE_Course_Spider(scrapy.Spider):
    name = "cee_course_spider"

    def start_requests(self):
        # craw multiple urls here
        yield scrapy.Request(url="https://www.polyu.edu.hk/cee/current-students/teaching-and-learning/syllabus/", callback=self.parse,
                             headers=head)

    def parse(self, response):
        # extract first 4 div whose class is "plus-collapse rte-template-collapse"
        course_container = response.css('div.plus-collapse.rte-template-collapse:nth-of-type(-n+4)')
        course_links = course_container.css('a::attr(href)').extract()
        filepath = 'cee_course_info.txt'
        with open(filepath, 'w') as f:
            f.writelines([c + "\n" for c in course_links if not c.startswith("#")])

class LSGI_Course_Spider(scrapy.Spider):
    name = "lsgi_course_spider"

    def start_requests(self):
        # craw multiple urls here
        yield scrapy.Request(url="https://www.polyu.edu.hk/lsgi/study/lsgi-subject-list/", callback=self.parse,
                             headers=head)

    def parse(self, response):
        course_container = response.css('div.plus-collapse.rte-template-collapse:nth-of-type(-n+4)')
        course_links = course_container.css('a::attr(href)').extract()
        filepath = 'lsgi_course_info.txt'
        with open(filepath, 'w') as f:
            f.writelines(["https://www.polyu.edu.hk" + c + "\n" for c in course_links if not c.startswith("#")])

# FENG (AAE, BME, COMP, EEE, ISE, ME)
class ME_Course_Spider(scrapy.Spider):
    name = "me_course_spider"

    def start_requests(self):
        yield scrapy.Request(url="https://www.polyu.edu.hk/me/study/course-info/subject-list/", callback=self.parse,
                             headers=head)

    def parse(self, response):
        course_container = response.css('table.static-table--less-padding-fullWidth--border-default--zebra')
        course_links = course_container.css('tbody > tr > td:nth-of-type(2) > a::attr(href)').extract()
        filepath = 'me_course_info.txt'
        for course_link in course_links:
            course_link = "https://www.polyu.edu.hk" + course_link
            with open(filepath, 'a') as f:
                f.write(course_link + "\n")

class BME_Course_Spider(scrapy.Spider):
    name = "bme_course_spider"

    def start_requests(self):
        # craw multiple urls here
        yield scrapy.Request(url="https://www.polyu.edu.hk/bme/study/undergraduate-programme/admissions/list-of-subjects-and-subject-description-forms/", callback=self.parse,
                             headers=head)

    def parse(self, response):
        course_container = response.css('table.static-table--less-padding')
        course_links = course_container.css('a::attr(href)').extract()
        filepath = 'bme_course_info.txt'
        with open(filepath, 'w') as f:
            f.writelines(["https://www.polyu.edu.hk" + c + "\n" for c in course_links])

class AAE_Course_Spider(scrapy.Spider):
    name = "aae_course_spider"

    def start_requests(self):
        # craw multiple urls here
        yield scrapy.Request(url="https://www.polyu.edu.hk/aae/study/subject-list/", callback=self.parse,
                             headers=head)

    def parse(self, response):
        course_container = response.css('div.border-hover-shadow-list')
        course_links = course_container.css('a::attr(href)').extract()
        filepath = 'aae_course_info.txt'
        for course_link in course_links:
            course_link = "https://www.polyu.edu.hk" + course_link
            with open(filepath, 'a') as f:
                f.write(course_link + "\n")

class CS_Course_Spider(scrapy.Spider):
    name = "comp_course_spider"

    def start_requests(self):
        # craw multiple urls here
        yield scrapy.Request(url="https://www.polyu.edu.hk/comp/study/ug-programmes/comp/subjects/",
                             callback=self.parse, headers=head)

    def parse(self, response):
        course_container = response.css('div.content')
        print(course_container)
        course_links = course_container.css('p > a::attr(href)').extract()

        filepath = 'cs_course_info.txt'
        with open(filepath, 'w') as f:
            f.writelines([c + "\n" for c in course_links])

class EIS_Course_Spider(scrapy.Spider):
    name = "eis_course_spider"

    def start_requests(self):
        # craw multiple urls here
        yield scrapy.Request(url="https://www.polyu.edu.hk/comp/study/ug-programmes/eis/subjects/", callback=self.parse,
                             headers=head)

    def parse(self, response):
        course_container = response.css('div.content')
        course_links = course_container.css('p > a::attr(href)').extract()
        filepath = 'eis_course_info.txt'
        with open(filepath, 'w') as f:
            f.writelines([c + "\n" for c in course_links])

class FTAI_Course_Spider(scrapy.Spider):
    name = "ftai_course_spider"

    def start_requests(self):
        # craw multiple urls here
        yield scrapy.Request(url="https://www.polyu.edu.hk/comp/study/ug-programmes/ftai/subjects/",
                             callback=self.parse, headers=head)

    def parse(self, response):
        course_container = response.css('div.content')
        print(course_container)
        course_links = course_container.css('p > a::attr(href)').extract()
        filepath = 'ftai_course_info.txt'
        with open(filepath, 'w') as f:
            f.writelines([c + "\n" for c in course_links])

class EEE_Course_Spider(scrapy.Spider):
    name = "eee_course_spider"

    def start_requests(self):
        # craw multiple urls here
        yield scrapy.Request(url="https://www.polyu.edu.hk/eee/study/information-for-current-students/subject-syllabi/", callback=self.parse,
                             headers=head)

    def parse(self, response):
        course_container = response.css('div.plus-collapse.rte-template-collapse')
        course_links = course_container.css('a::attr(href)').extract()
        filepath = 'eee_course_info.txt'
        with open(filepath, 'w') as f:
            f.writelines(["https://www.polyu.edu.hk" + c + "\n" for c in course_links if not c.startswith("#") and c.startswith("/")])

class ISE_Course_Spider(scrapy.Spider):
    name = "ise_course_spider"

    def start_requests(self):
        # craw multiple urls here
        yield scrapy.Request(url="https://www.polyu.edu.hk/ise/study/information-for-current-students/programme-related-info/subject-syllabi/", callback=self.parse,
                             headers=head)

    def parse(self, response):
        course_container = response.css('div.container.static-content.color-set--feng')
        course_links = course_container.css('a::attr(href)').extract()
        filepath = 'ise_course_info.txt'
        with open(filepath, 'w') as f:
            f.writelines(["https://www.polyu.edu.hk" + c + "\n" for c in course_links])

# FS (ABCT, AMA, AP, FSN)
class ABCT_Course_Spider(scrapy.Spider):
    name = "abct_course_spider"

    def start_requests(self):
        # craw multiple urls here
        yield scrapy.Request(url="https://www.polyu.edu.hk/abct/study/undergraduate-programmes/list-of-all-subjects_ug/", callback=self.parse,
                             headers=head)

    def parse(self, response):
        course_container = response.css('div.container.static-content.color-set--fast')
        course_links = course_container.css('a::attr(href)').extract()
        filepath = 'abct_course_info.txt'
        with open(filepath, 'w') as f:
            f.writelines(["https://www.polyu.edu.hk" + c + "\n" for c in course_links])

class AMA_Course_Spider(scrapy.Spider):
    name = "ama_course_spider"

    def start_requests(self):
        # craw multiple urls here
        yield scrapy.Request(url="https://www.polyu.edu.hk/ama/study/subject-library/", callback=self.parse,
                             headers=head)

    def parse(self, response):
        course_container = response.css('div.plus-collapse.rte-template-collapse:nth-of-type(-n+4)')
        course_links = course_container.css('a::attr(href)').extract()
        filepath = 'ama_course_info.txt'
        with open(filepath, 'w') as f:
            f.writelines([c + "\n" for c in course_links if not c.startswith("#")])

class AMA_Car_Spider(scrapy.Spider):
    name = "ama_car_spider"

    def start_requests(self):
        # craw multiple urls here
        yield scrapy.Request(url="https://www.polyu.edu.hk/ama/study/cluster-area-requirements-and-service-learning/", callback=self.parse,
                             headers=head)

    def parse(self, response):
        course_container = response.css('table.static-table--fullWidth--border--no-zebra')
        course_links = course_container.css('a::attr(href)').extract()
        filepath = 'ama_car_info.txt'
        with open(filepath, 'w') as f:
            f.writelines([c + "\n" for c in course_links if not c.startswith("#")])

class AP_Course_Spider(scrapy.Spider):
    name = "ap_course_spider"

    def start_requests(self):
        # craw multiple urls here
        yield scrapy.Request(url="https://www.polyu.edu.hk/ap/study/subject-list/bachelor-programme//", callback=self.parse,
                             headers=head)

    def parse(self, response):
        course_container = response.css('table.static-table--less-padding-fullWidth--border-default--no-zebra')
        # extract the tr elements' data-href
        course_links = course_container.css('tr[data-href]::attr(data-href)').extract()
        filepath = 'ap_course_info.txt'
        with open(filepath, 'w') as f:
            f.writelines(["https://www.polyu.edu.hk" + c + "\n" for c in course_links if not c.startswith("#")])

class FSN_Course_Spider(scrapy.Spider):
    name = "fsn_course_spider"

    def start_requests(self):
        # craw multiple urls here
        yield scrapy.Request(url="https://www.polyu.edu.hk/fsn/study/list-of-all-subjects/", callback=self.parse,
                             headers=head)

    def parse(self, response):
        course_container = response.css('table.static-table--normal--border-default--no-zebra')
        course_links = course_container.css('a::attr(href)').extract()
        filepath = 'fsn_course_info.txt'
        with open(filepath, 'w') as f:
            f.writelines([c + "\n" for c in course_links if not c.startswith("#")])

# FH (CHC, CBS, ENGL)
class CHC_Course_Spider(scrapy.Spider):
    name = "chc_course_spider"

    def start_requests(self):
        # craw multiple urls here
        yield scrapy.Request(url="https://www.polyu.edu.hk/chc/study/courses-offering/?sc_lang=tc", callback=self.parse,
                             headers=head)

    def parse(self, response):
        # extract first two div whose class is "plus-collapse rte-template-collapse"
        course_container = response.css('div.plus-collapse.rte-template-collapse:nth-of-type(-n+2)')
        course_links = course_container.css('a::attr(href)').extract()
        filepath = 'chc_course_info.txt'
        with open(filepath, 'w') as f:
            f.writelines(["https://www.polyu.edu.hk" + c + "\n" for c in course_links if not c.startswith("#")])

class CBS_Car_Spider(scrapy.Spider):
    name = "cbs_car_spider"

    def start_requests(self):
        # craw multiple urls here
        yield scrapy.Request(url="https://www.polyu.edu.hk/cbs/study/undergraduate-programmes/gur-subjects-offered-by-cbs/cluster-area-requirements", callback=self.parse,
                             headers=head)

    def parse(self, response):
        course_container = response.css('div.ITS_Content_TextImage_5Links  ')
        course_links = course_container.css('a::attr(href)').extract()
        filepath = 'cbs_car_info.txt'
        with open(filepath, 'w') as f:
            f.writelines([c + "\n" for c in course_links if not c.startswith("#")])

class CBS_SL_Spider(scrapy.Spider):
    name = "cbs_sl_spider"

    def start_requests(self):
        # craw multiple urls here
        yield scrapy.Request(url="https://www.polyu.edu.hk/cbs/study/undergraduate-programmes/gur-subjects-offered-by-cbs/service-learning", callback=self.parse,
                             headers=head)

    def parse(self, response):
        course_container = response.css('div.ITS_Content_TextImage_5Links  ')
        course_links = course_container.css('a::attr(href)').extract()
        filepath = 'cbs_sl_info.txt'
        with open(filepath, 'w') as f:
            f.writelines([c + "\n" for c in course_links if not c.startswith("#")])

class ENGL_Course_Spider(scrapy.Spider):
    name = "engl_course_spider"

    def start_requests(self):
        # craw multiple urls here
        yield scrapy.Request(url="https://www.polyu.edu.hk/engl/study/full-subject-list/", callback=self.parse,
                             headers=head)

    def parse(self, response):
        course_container = response.css('div.plus-collapse.rte-template-collapse:nth-of-type(-n+4)')
        course_links = course_container.css('a::attr(href)').extract()
        filepath = 'engl_course_info.txt'
        with open(filepath, 'w') as f:
            f.writelines(["https://www.polyu.edu.hk" + c + "\n" for c in course_links if not c.startswith("#")])

# FHS

# SHTM
class SHTM_Course_Spider(scrapy.Spider):
    name = "shtm_course_spider"

    def start_requests(self):
        # craw multiple urls here
        base_url = "https://www.polyu.edu.hk/shtm/study/subject-syllabi/?category=Undergraduate&keyword=&page="
        pages = range(1, 10)  # Pages 1 to 9
        urls = [base_url + str(page) for page in pages]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, headers=head)

    def parse(self, response):
        course_container = response.css('table.static-table--less-padding-fullWidth--border-default--zebra')
        course_links = course_container.css('tr[data-href]::attr(data-href)').extract()
        filepath = 'shtm_course_info.txt'
        with open(filepath, 'a') as f:
            for course_link in course_links:
                if course_link.startswith("/"):
                    course_link = "https://www.polyu.edu.hk" + course_link
                f.write(course_link + "\n")



process = CrawlerProcess()
# process.crawl(ME_Course_Spider)
# process.crawl(CS_Course_Spider)
# process.crawl(EIS_Course_Spider)
# process.crawl(FTAI_Course_Spider)
# process.crawl(AF_Course_Spider)
# process.crawl(APSS_Course_Spider)
# process.crawl(AAE_Course_Spider)
# process.crawl(LMS_Course_Spider)
# process.crawl(MM_Course_Spider)
# process.crawl(BRE_Course_Spider)
# process.crawl(CEE_Course_Spider)
# process.crawl(LSGI_Course_Spider)
# process.crawl(BME_Course_Spider)
# process.crawl(ISE_Course_Spider)
# process.crawl(EEE_Course_Spider)
# process.crawl(ABCT_Course_Spider)
# process.crawl(AMA_Course_Spider)
# process.crawl(AMA_Car_Spider)
# process.crawl(AP_Course_Spider)
# process.crawl(FSN_Course_Spider)
# process.crawl(CHC_Course_Spider)
# process.crawl(CBS_Car_Spider)
# process.crawl(CBS_SL_Spider)
# process.crawl(ENGL_Course_Spider)
# process.crawl(SHTM_Course_Spider)
process.start()
