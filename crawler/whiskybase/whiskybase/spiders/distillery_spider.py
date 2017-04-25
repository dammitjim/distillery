import scrapy
import re


class DistillerySpider(scrapy.Spider):
    name = "distilleries"
    start_urls = [
        "https://www.whiskybase.com/distilleries",
    ]

    whisky_href_re = re.compile("/[0-9]+/")

    def parse(self, response):
        for distillery in response.css(".whiskytable tbody tr a::attr(href)").extract():
            yield scrapy.Request(distillery, callback=self.parse_distillery)
        nxt = response.css(".pagination li:last-child a::attr(href)").extract_first()
        if nxt:
            yield scrapy.Request(nxt, callback=self.parse)

    def parse_distillery(self, response):
        name = response.css('#distillery-info h1 span::text').extract_first()
        address_raw = response.css('.maps-address::text').extract()

        address = ""
        if len(address_raw) > 0:
            address = ", ".join([addr.strip() for addr in address_raw])

        data_dict = {
            "name": name,
            "address": address,
            "url": response.url,
        }

        for stat in response.css('#distillery-stats .stat-item'):
            data = stat.css('.data::text').extract_first()
            key = stat.css('.key::text').extract_first()
            if key and data:
                data_dict[key] = data

        for stat in response.css('.stats-horizontal .stat-item'):
            data = stat.css('.data::text').extract_first()
            key = stat.css('.key::text').extract_first()
            if key and data:
                data_dict[key] = data

        whisky_hrefs = response.css('.whiskytable tr .whisky-name a::attr(href)').extract()
        data_dict["whiskies"] = [
            wid.group(0).replace("/", "") for href in whisky_hrefs for wid in [self.whisky_href_re.search(href)] if wid]

        yield data_dict
