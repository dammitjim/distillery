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
        addresses = response.css('.maps-address')
        address = self._get_full_address(addresses)

        if not name:
            return

        if not address:
            return

        data_dict = {
            "name": name,
            "address": address,
            "url": response.url,
        }

        wb_id = self.whisky_href_re.search(response.url)
        if wb_id:
            data_dict["wb_id"] = wb_id.group(0).replace("/", "")

        for stat in response.css('#distillery-stats .stat-item'):
            data = stat.css('.data *::text').extract_first()
            key = stat.css('.key *::text').extract_first()
            if key and data:
                data_dict[key.lower()] = data

        for stat in response.css('.stats-horizontal .stat-item'):
            data = stat.css('.data *::text').extract_first()
            key = stat.css('.key *::text').extract_first()
            if key and data:
                data_dict[key.lower()] = data

        whisky_hrefs = response.css('.whiskytable tr .whisky-name a::attr(href)').extract()
        data_dict["whiskies"] = [
            wid.group(0).replace("/", "") for href in whisky_hrefs for wid in [self.whisky_href_re.search(href)] if wid]

        yield data_dict

    @staticmethod
    def _get_full_address(addresses):
        address = ""
        # some pages have duplicate maps address, dont know why
        if len(addresses) > 0:
            address_raw = addresses[0].css('*::text').extract()
            address = ", ".join([addr.strip() for addr in address_raw])
        return address
