import scrapy
from scrapy_splash import SplashRequest
import logging
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
#from tfrrspipeline.items import TFRRSpipelineItem
from tfrrspipeline.items import athletepipelineItem

# Get Brendan's team urls
with open("/Users/dmcdonnell/Desktop/conf_team_links.csv") as f:
    s = f.read() + '\n'
s = s.split()
s = s[1:2]
brendanurl = ['https:' + i for i in s]

# Run spider
class ResultSpider(scrapy.Spider):
    name = 'tfrrs2'

    script = '''
function main(splash, args)
  assert(splash:go(args.url))
  while not splash:select('select.form-control') do
    splash:wait(0.1)
  end

  treat = require('treat')
  input = splash:select('select.form-control')
 	season = splash:select('option[selected]').innerHTML
  input:click()

  if splash.args.n == 0 then
  else
 		for i = 0, splash.args.n -1 do
    	input:send_keys("<Down>")
  	end
  end
  input:send_keys("<Enter>")
  maxwait = 5
  i = 1
  season2 = splash:select('option[selected]').innerHTML
	while season == season2 do
    if i == maxwait then
      break
    end
    i = i + 1
    splash:wait(1)
    season2 = splash:select('option[selected]').innerHTML
  end
	while splash:select('td.tablesaw-priority-persist a') == nil do
    splash:wait(.1)
  end

  if not splash:select_all("div div.col-lg-4 tbody a") then
    elems = ''
  else
    elems = splash:select_all("div div.col-lg-4 tbody a")
    hrefs = {}
    for i, elem in ipairs(elems) do
      hrefs[i] = elem.node:getAttribute("href")
    end
  end

  return treat.as_array(hrefs), season2
end
'''
  #also need to return team, season from dropdown, athlete name, athlete grade
  #send to pipeline to make new table for this data

# Start spider requests
    def start_requests(self):
        n = 26
        for url in brendanurl:
            for i in range(n):
                yield SplashRequest(url=url, callback=self.parse_other_pages, endpoint='execute', args={'lua_source': self.script, "n": i}, dont_filter = True)

    def parse_other_pages(self, response):
        athleteitem = athletepipelineItem()
        athleteitem['Season'] = response.xpath('option[selected]').get().strip()
        for i in range(len(response.data)):
            yield response.follow(url = response.data[i], callback = self.parse2)

        # Get athlete data, append it to all other athlete data in a dataframe
    def parse2(self, response):
        #Full page container
        Page = response.xpath('//div[@class = "page container"]')

        #Meet results container
        allresults = response.xpath('//div[@id = "meet-results"]')

        #Count the divs containing each meet's info
        divs = allresults.xpath('./div')

        #Scrape and store the data
        title = page.xpath('.//div[@class = "panel-heading"]/a[1]//h3//text()').get().strip().title().splitlines()

        # Name of items to scrape
        item = TFRRSpipelineItem()

        for i in range(len(divs)):
            place = [s.replace('\xa0\n', ' ') for s in allresults.xpath('./div['+str(i+1)+']//tr/td[3]/text()').getall()]
            events = [s.strip() for s in allresults.xpath('./div['+str(i+1)+']//tr/td[1]/text()').getall()]
            performance = [s.strip() for s in allresults.xpath('./div['+str(i+1)+']//tr/td[2]/a/text()').getall()]

            if enumerate(events) == 0:
                item['AthleteName'] = title[0]
                item['Team'] = ''
                item['Location'] = ''
                item['EventDate'] = ''
                item['Event'] = ''
                item['Performance'] = ''
                item['Place'] = ''
                yield item
            else:
                for index, event in enumerate(events):
                    item['AthleteName'] = title[0]
                    item['Team'] = page.xpath('.//div[@class = "panel-heading"]/a[3]/h3/text()').get().strip().title()
                    item['Location'] = allresults.xpath('./div['+str(i+1)+']//th//a/text()').get().strip()
                    item['EventDate'] = allresults.xpath('./div['+str(i+1)+']//th//span/text()').get().strip()
                    item['Event'] = events[index]
                    item['Performance'] = performance[index]
                    item['Place'] = [s.strip() for s in place][index]
                    yield item
