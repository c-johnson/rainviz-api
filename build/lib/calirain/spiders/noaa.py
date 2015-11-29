import scrapy
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst
from urlparse import urljoin

class Rainfall(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    precipValues = scrapy.Field()

class NoaaSpider(scrapy.Spider):
    name = "calirain"
    allowed_domains = ["www.cnrfc.noaa.gov"]
    start_urls = ['http://www.cnrfc.noaa.gov/awipsProducts/RNORR5RSA.php']
    delims = [":", ".", "$", ""]
    precipData = []

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        rowStrings = response.css('.center-content pre')[0].extract().split("\n")
        rowStrings = rowStrings[3:]
        for row in rowStrings:
            if row[0] in self.delims: continue
            parts = row.split(" : ")
            if len(parts) < 3: continue
            id = parts[0]
            name = parts[1]
            rawPrecip = parts[2].split("/ ")
            precipBuckets = {
                'oneHour': rawPrecip[0],
                'twoHour': rawPrecip[1],
                'threeHour': rawPrecip[2],
                'sixHour': rawPrecip[3],
                'twelveHour': rawPrecip[4],
                'daily': rawPrecip[5]
            }
            precipRow = Rainfall(id=id, name=name, precipValues=precipBuckets)
            self.precipData.append(precipRow)
            # print precipRow
            # self.logger.info(precipRow)

        # self.logger.info(len(rowStrings))
        # self.logger.info("hello!!!!!!!")
        return self.precipData

# class CompanyLoader(ItemLoader):
#     default_input_processor = MapCompose(unicode.strip)
#     default_output_processor = TakeFirst()

# arr.map(function(item) {
#   console.log(JSON.stringify(item));
#   var parts = item.split(" : ");
#   var id = parts[0];
#   var name = parts[1];
#   var rawPrecip = parts[2];
#   precipBuckets = rawPrecip.split("/ ");
#   var precipRow = {
#     id: id,
#     name: name,
#     precip: precipBuckets
#   };
#   precipData.push(precipRow);
#   // console.log("id = " + id + "\nname = " + name + "\nprecip = " + JSON.stringify(precipBuckets))

        # var arr = $('.center-content pre').text().split('\n');
        # arr.splice(0, 3);
        # arr = arr.filter(function(item) { return delims.indexOf(item.charAt(0)) === -1 });

        # with open(filename, 'wb') as f:
            # f.write(filetext)

    # def parse(self, response):
    #     for x in response.xpath("//table[@class='col2_table_listing']//a/@href").extract():
    #         yield scrapy.Request(urljoin(response.url, x), self.parse_company)
    #
    # def parse_company(self, response):
    #     l = CompanyLoader(item=Company(), response=response)
    #     l.add_xpath("logo", "//div[@id='company_logo']//img/@src")
    #     l.add_xpath("name", "//h1[@class='h1_first']/text()")
    #     l.add_xpath("website", "(//td[@class='td_right']/a/@href)[1]")
    #     return l.load_item()
