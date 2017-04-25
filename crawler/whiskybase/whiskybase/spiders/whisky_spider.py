import scrapy


class WhiskySpider(scrapy.Spider):
    name = "whisky"
    start_urls = [
        "https://www.whiskybase.com/brands",
    ]

    def parse(self, response):
        for brand in response.css(".whiskytable tbody tr a::attr(href)").extract():
            yield scrapy.Request(brand, callback=self.parse_brand)
        next_page = response.css(".pagination li:last-child a::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_brand(self, response):
        brand_name = response.css("#distillery-info h1 span::text").extract_first()
        whiskys = response.css(".whiskytable tbody tr .whisky-name a::attr(href)")
        for whisky in whiskys.extract():
            yield scrapy.Request(whisky, callback=self.parse_whisky, meta={"brand": brand_name})
        next_page = response.css('.pagination li:last-child a::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse_brand)

    def parse_whisky(self, response):
        whisky_name = response.css(".whisky-name::text").extract_first()
        data_dict = {
            "name": whisky_name,
            "brand": response.meta["brand"],
            "url": response.url,
        }

        for tr in response.css("table.winfo tr"):
            row = tr.css('td *::text').extract()
            cleaned = [data.strip() for data in row]
            if len(cleaned) == 0:
                continue

            key = cleaned[0]
            if key == "":
                continue

            value = " ".join([x for x in cleaned if x != ""])
            if value.startswith(key):
                value = value.replace(key, "", 1).strip()

            key = self._key_override(key)

            data_dict[key] = value

        yield data_dict

    @staticmethod
    def _key_override(key):
        lookup = key.lower()
        override = {
            "bottling serie": "bottling series",
        }.get(lookup)
        if override:
            return override
        return lookup
