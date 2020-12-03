import scrapy
import re
from scrapy.crawler import CrawlerProcess

class FifaSpider(scrapy.Spider):
    name = "get_players_urls"

    def __init__(self):
        self.pages = 0
        self.counter = 0

    def start_requests(self):

        # All fifa player data urls in chronological order from FIFA 07 to FIFA 21
        urls = {'https://sofifa.com/players?r=070002&set=true',
        'https://sofifa.com/players?r=080002&set=true'
        } 

        # ,
        # 'https://sofifa.com/players?r=090002&set=true',
        # 'https://sofifa.com/players?r=100002&set=true',
        # 'https://sofifa.com/players?r=110002&set=true',
        # 'https://sofifa.com/players?r=120002&set=true',
        # 'https://sofifa.com/players?r=130034&set=true',
        # 'https://sofifa.com/players?r=140052&set=true',
        # 'https://sofifa.com/players?r=150059&set=true',
        # 'https://sofifa.com/players?r=160058&set=true',
        # 'https://sofifa.com/players?r=170099&set=true',
        # 'https://sofifa.com/players?r=180084&set=true',
        # 'https://sofifa.com/players?r=190075&set=true',
        # 'https://sofifa.com/players?r=200061&set=true',
        # 'https://sofifa.com/players?r=210015&set=true'
       

        for url in urls:
            yield scrapy.Request(url=url, callback = self.parse)

    def parse(self, response):
        print(self.pages)
        year_id = re.findall(r'\d+', response.url)[0]
        for player in response.css('.col-name'):
            if len(player.xpath('a/@href').re('[0-9]+')) == 0: # if list is empty
                pass
            elif len(player.xpath('a/@href').re('[0-9]+')) == 1: # if list contains the only the unique identifier for the FIFA Year
                pass
            else: 
                player_id = player.xpath('a/@href').re('[0-9]+')[0] # all else contains the actual player IDs
                player_url = "https://sofifa.com/player/" + str(player_id) + "/" + str(year_id)
                yield {
                    'player_url': player_url
                }


        next_page = response.xpath('.//a[@class="bp3-button pjax"]/@href').extract()
        if next_page:
            if len(next_page) == 1:
                next_href = next_page[0]
                next_page_url = 'https://sofifa.com' + next_href
            else:
                next_page_url  = urls[self.counter]
                self.counter += 1
            self.pages += 1
            request = scrapy.Request(url=next_page_url)
            yield request

# if __name__ == "__main__":
#   process = CrawlerProcess()
#   process.crawl(FifaSpider)
#   process.start()

# scrapy crawl get_players_urls -t json -o outputfile.json

# scrapy crawl FifaSpider -t csv -o outputfile.csv