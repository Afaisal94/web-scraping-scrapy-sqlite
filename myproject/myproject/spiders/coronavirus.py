import scrapy


class CoronavirusSpider(scrapy.Spider):
    name = 'coronavirus'
    allowed_domains = ['worldometers.info']
    start_urls = ['https://www.worldometers.info/coronavirus/']

    def parse(self, response):
        countries = response.xpath("//a[@class='mt_a']")
        for country in countries:
            name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()

            yield response.follow(url=link, callback=self.parse_country, meta={'country_name': name})

    def parse_country(self, response):
        name = response.request.meta['country_name']
        coronavirus_cases = response.xpath("//div[@class='content-inner']/div[4]/div/span/text()").get()
        deaths = response.xpath("//div[@class='content-inner']/div[5]/div/span/text()").get()
        recovered = response.xpath("//div[@class='content-inner']/div[6]/div/span/text()").get()

        yield {
            'country_name': name,
            'coronavirus_cases': coronavirus_cases,
            'deaths': deaths,
            'recovered': recovered
        }