import scrapy
import xml.etree.cElementTree as ET
import datetime


sitemap = []


class BlogSpider(scrapy.Spider):
    name = 'DDW'
    download_delay = 2.0
    start_urls = 'http://localhost:8000/'
    citiesCrawled = {}
    personsCrawled = {}
    

    def start_requests(self):
        yield scrapy.Request(self.start_urls, callback=self.parseCities, headers={"User-Agent": "DDW"})

    def parsePersonsInfo(self, response):
        personInfo = {}
        for span in response.css('div.person  span'):
            personInfo[span.css('::attr(class)').get()] = span.css('::text').get()
        yield personInfo

        for other_city in response.css('ul.cities li'):
            yield scrapy.Request(response.urljoin(other_city.css('a::attr(href)').extract_first()), callback=self.parseCities, headers={"User-Agent": "DDW"})

    def parsePersons(self, response):
        for li in response.css('ul.persons  li'):
            next_person = li.css('a::attr(href)').extract_first()
            print(response.urljoin(next_person))
            if next_person and next_person not in self.personsCrawled:
                self.personsCrawled[next_person] = 1
                sitemap.append(next_person)
                yield {'city': response.meta.get('city'), 'person': li.css('a::text').extract_first()}
                yield scrapy.Request(response.urljoin(next_person), callback=self.parsePersonsInfo, headers={"User-Agent": "DDW"})
        
        for other_city in response.css('ul.cities li'):
            yield scrapy.Request(response.urljoin(other_city.css('a::attr(href)').extract_first()), callback=self.parseCities, headers={"User-Agent": "DDW"})


    def parseCities(self, response):
        for li in response.css('ul.cities  li'):
            next_city = li.css('a::attr(href)').extract_first()
            city_name = li.css('a::text').extract_first()
            print(response.urljoin(next_city))
            if next_city and next_city not in self.citiesCrawled:
                self.citiesCrawled[next_city] = 1
                sitemap.append(next_city)
                yield {'city': city_name}
                yield scrapy.Request(response.urljoin(next_city), callback=self.parsePersons, meta={'city': city_name}, headers={"User-Agent": "DDW"})

    def closed( self, reason ):

        root = ET.Element("root")
        
        for item in sorted(sitemap, key=str.lower):
            url = ET.SubElement(root, "url")

            ET.SubElement(url, "loc").text = item
            ET.SubElement(url, "lastmod").text = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")

        tree = ET.ElementTree(root)
        tree.write("sitemap.xml")


