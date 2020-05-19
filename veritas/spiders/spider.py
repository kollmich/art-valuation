from scrapy.http import FormRequest
from scrapy import Request
from scrapy.crawler import CrawlerProcess

from veritas.items import VeritasItem

import scrapy

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'FEED_FORMAT': 'json',
    'FEED_URI': 'result.json'
})

class LoginSpider(scrapy.Spider):
    name = 'veritas'
    start_urls = ['https://veritas.art/wp-login.php']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'log': 'koll44@gmail.com', 'pwd': 'bonham'},#, 'action': 'loginUser', 'nonce': '45e0196df6'},
            callback=self.after_login 
        )

    def after_login(self, response):
        if b": The username or password you entered is incorrect." in response.body:
            self.logger.error("Login failed!")
        else:
            self.logger.error("Login succeeded!")
            return Request(url="https://veritas.art/auctions/previous/", callback=self.parse_auctions)

    def parse_auctions(self, response):
        print('parsing auctions...')
        AUCTION_SELECTOR = '.card-auction__call-to-action.see-post-call.js-see-post-call.link.-nocolor.uk-padding-small::attr(href)'
        auctions = response.css(AUCTION_SELECTOR).getall()
        print(auctions[0:1])
        for a in auctions[0:1]:
            yield Request(url=a + "/?posts_per_page=10000&current_page=1", callback=self.parse_lots)
            # print(a)

    def parse_lots(self, response):
        print('parsing lots...')
        LOT_SELECTOR = 'div.lot__name'
        lots = response.css(LOT_SELECTOR).css('a::attr(href)').getall()
        for lot in lots:
            yield Request(url= lot, callback=self.parse_lot)
            # print(lot)


    def parse_lot(self, response):
        print('parsing lot...')
        SET_SELECTOR = '.lot-section'
        for lot in response.css(SET_SELECTOR):
            NAME_SELECTOR = 'h2.title.name ::text'
            AUTHOR_SELECTOR = 'h3.title.-fancy.author ::text'
            ESTIMATE_SELECTOR = '//*[@id="main"]/article/div/section[2]/div/div[1]/p/text()'
            SESSION_SELECTOR = '//*[@id="main"]/article/div/section[2]/div/div[2]/p/text()'
            HAMMER_SELECTOR = '//*[@id="main"]/article/div/section[2]/div/div[3]/span/text()'
            DESCRIPTION_SELECTOR = '//*[@id="main"]/article/div/section[2]/div/div[4]/p[1]/text()'
            SIZE_SELECTOR = '//*[@id="main"]/article/div/section[2]/div/div[4]/p[2]/text()'
            CATEGORY_SELECTOR = '//*[@id="main"]/article/div/section[2]/div/div[5]/p/span/text()'
            IMAGE_SELECTOR = 'img.js-zoom-img ::attr(data-src)'

            item = VeritasItem()

            item['name'] = lot.css(NAME_SELECTOR).get(),#.replace('\n','').replace('\t',''),
            item['author'] = lot.css(AUTHOR_SELECTOR).get(),#.replace('\n','').replace('\t',''),
            item['price_estimate'] = lot.xpath(ESTIMATE_SELECTOR).get().replace('\n','').replace('\t',''),
            item['session_date'] = lot.xpath(SESSION_SELECTOR).get().replace('\n','').replace('\t',''),
            item['price_hammer'] = lot.xpath(HAMMER_SELECTOR).get().replace('\n','').replace('\t',''),
            item['description'] = lot.xpath(DESCRIPTION_SELECTOR).getall(),
            item['size'] = lot.xpath(SIZE_SELECTOR).getall(),#.replace('\n','').replace('\t',''),
            item['category'] = lot.xpath(CATEGORY_SELECTOR).get(),#.replace('\n','').replace('\t',''),
            item['image'] = lot.css(IMAGE_SELECTOR).get()

            yield item