# import scrapy
# from scrapy.crawler import CrawlerProcess
# from scrapy.http import FormRequest
# import requests
# from bs4 import BeautifulSoup
#
# class Mainland_WIE_Web_Spider(scrapy.Spider):
#     name = "mainland_wie_spider"
#
#     def start_requests(self):
#         login_url = 'https://adfs.polyu.edu.hk/adfs/ls/?SAMLRequest=fZJBT4MwGIb%2FCukd2lWysGaQ4HZwyVQy0IMXU6AbjaVFviLbvxeGU3fZtX37vN%2F3pEvgtWpY3NlK78RnJ8A6x1ppYOeLEHWtZoaDBKZ5LYDZgqXx45ZRj7CmNdYURiEnBhCtlUavjIauFm0q2i9ZiJfdNkSVtQ0wjPu%2B9xqjTp0nys6rPnBayTw3StjKAzD6gEcyxclzmiFnPYwiNR%2Bhfwhe7uGaMZ5gBRg5m3WI3mkeUFIGxYzcFXuyCHxf%2BJSLvU8CQubzxRAD6MRGg%2BXahogS6ruEusTPZoT5PqPBG3KSn8XupS6lPty2kE8hYA9ZlrjT8K%2BihfPgQwBFy9ElOxe3%2F%2BzexvKLUhRdttcHqY8uDNauHcCvxyX%2BVzX1NuxpYG%2FWiVGyODmxUqZftYJbEaIZwtH05PoLRN8%3D&RelayState=ss%3Amem%3A588bfa2021961017f807994a0e9ed2eb255247381c406cbfcced6db0e98dc9c6'
#         target_url = 'https://www.polyu.edu.hk/sao/internal/careers-and-placement-section/mainland-wie/'
#
#         # Provide your username and password
#         username = '22099687d'
#         password = 'Dhhdwh88'
#
#         # Create a session to handle cookies and maintain the session
#         session = requests.Session()
#
#         # Send a GET request to the login URL to get the initial cookies
#         response = session.get(login_url)
#         soup = BeautifulSoup(response.text, 'html.parser')
#
#         # Extract the required form data (input field names and values)
#         form_data = {}
#         for input_field in soup.find_all('input'):
#             if input_field.get('name'):
#                 form_data[input_field['name']] = input_field.get('value', '')
#
#         # Update the form data with the username and password
#         form_data['username'] = username
#         form_data['password'] = password
#
#         # Send a POST request with the form data for authentication
#         response = session.post(login_url, data=form_data)
#
#         # Scrape the target URL
#         yield scrapy.Request(url=target_url, callback=self.parse, cookies=session.cookies.get_dict())
#
#     def parse(self, response):
#         # Get all the pure text inside <main class="page-content">
#         text = response.css("main.page-content ::text").getall()
#         print(len(text))
#         # pure_text = ' '.join(text).strip()
#         # pure_text = pure_text.replace('\n', ' ').replace('  ', ' ')
#         # filepath = 'mainland_wie_info.txt'
#         # with open(filepath, 'w') as f:
#         #     f.write(pure_text)
#
#
# process = CrawlerProcess()
#
# process.crawl(Mainland_WIE_Web_Spider)
#
# process.start()
