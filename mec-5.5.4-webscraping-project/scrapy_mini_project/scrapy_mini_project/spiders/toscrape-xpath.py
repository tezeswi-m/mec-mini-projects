import scrapy


class AuthorSpider(scrapy.Spider):
    name = 'toscrape-xpath'

    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        author_page_links = response.xpath('//div[@class="quote"]/span/a/@href')

        self.logger.info('Parse function called on %s', author_page_links)
        yield from response.follow_all(author_page_links, self.parse_author)

        pagination_links = response.xpath('//li[@class = "next"]/a/@href')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        self.logger.info('Parse called on %s', response)

        def extract_with_xpath(query):
            return response.xpath(query).get(default='').strip()

        print(response, '\n\n')

        yield {
            'name': extract_with_xpath('/h3[@class = "author-title"]/text()'),
            'birthdate': extract_with_xpath('//h3[@class="author-title"]/text()'),
            'bio': extract_with_xpath('//div/div[@class="author-description"]/text()'),
        }