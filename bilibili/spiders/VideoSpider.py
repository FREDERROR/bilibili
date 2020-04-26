import scrapy
import time
import json
from scrapy.conf import settings
from bilibili.items import VideoItem
from scrapy.http import Request,Response


class VideoSpider(scrapy.Spider):
    name = 'video'
    allowed_domains = ['bilibili.com']
    start_urls = ['http://www.bilibili.cexiom/']
    spider_av = range(settings.get("VIDEO_START"),settings.get("VIDEO_END"))

    def start_requests(self):
        for av in self.spider_av:
            video_header = {
                "HOST":"www.bilibili.com",
                "Accept":"text/html,application",
                "Accept-Language":"en-US,en;q=0.5",
                "USER-AGENT":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
            }
            print(f"爬取 av{av}")
            video_request = scrapy.Request(url=f"https://www.bilibili.com/video/av{av}",
                                           headers = video_header,
                                           callback=self.parse_video_page
                                           )
            yield video_request
    def parse(self, response):
        if json.loads(response.body)['code'] == 0:
            data = json.loads(response.body)['data']
            item = response.request.meta['item']
            item['view'] = data['view']
            item['danmaku'] = data['danmaku']
            item['reply'] = data['reply']
            item['favorite'] = data['favorite']
            item['coin'] = data['coin']
            item['share'] = data['share']
            item['like'] = data['like']
            item['now_rank'] = data['now_rank']
            item['his_rank'] = data['his_rank']
            if item['view'] > 100000:
                return item

    def parse_video_page(self,response:Response):
        item = VideoItem()
        item['up_name'] = response.css('.name a::text').extract_first()
        item['title'] = response.css('.tit::text').extract_first()
        aid = response.url.replace("https://www.bilibili.com/video/av","")
        item['aid'] = aid.replace("/","")
        timestamp = int(round(time.time()*1000))
        header = {
            "Host":"api.bilibili.com",
            "Origin":"https: // www.bilibili.com",
            "Referer": f"https://www.bilibili.com/video/av{item['aid']}/",
            "USER-AGENT":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        }
        yield Request(
            url=f"http://api.bilibili.com/archive_stat/stat?callback=&aid={item['aid']}&type=json&_={timestamp}",
            dont_filter=False,
            headers = header,
            callback=self.parse,
            meta = {"item": item}
        )
