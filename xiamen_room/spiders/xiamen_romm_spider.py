# -*- coding: utf-8 -*-
import scrapy
from xiamen_room.items import XiamenRoomItem

class XiamenRommSpiderSpider(scrapy.Spider):
    name = 'xiamen_romm_spider'
    # allowed_domains = ['fdc.xmtfj.gov.cn:8001']
    # start_urls = ['http://movie.douban.com/top250']

    def start_requests(self):
        all_json = [
            {
                'BuildID': '6000024056',
                'NAID': '1000012510',
                'lotid': '137842',
                't': '1537063206615'
            },
            {
                'BuildID': '6000024058',
                'NAID': '1000012510',
                'lotid': '137842',
                't': '1537063235230'
            }
        ]

        for json_item in all_json:
            yield scrapy.FormRequest(
                url='http://fdc.xmtfj.gov.cn:8001/Lp/LPPartial',
                formdata=json_item,
                callback=self.alldata
            )

    def alldata(self, response):
        all_id = []
        # item_id = response.xpath("//div//table//tr//td[@class='fw_tddy  hand']/@id")
        item_id = response.xpath("//div//table//tr//td/@id")
        for i_item in item_id:
            all_id.append(i_item.extract())
            yield scrapy.Request("http://fdc.xmtfj.gov.cn:8001/LP/Fwztxx?HouseId="+i_item.extract(), callback=self.parse)
        print(all_id)

    def parse(self, response):
        all_list = response.xpath("//div//table//tr")
        xiamen_item = XiamenRoomItem()
        try:
            # has_data = all_list[6]
            xiamen_item['address'] = all_list[0].xpath(".//td[2]/text()").extract_first()
            xiamen_item['room_id'] = all_list[1].xpath(".//td[2]/text()").extract_first()
            xiamen_item['property'] = all_list[2].xpath(".//td[2]/text()").extract_first()
            xiamen_item['use'] = all_list[3].xpath(".//td[2]/text()").extract_first()
            xiamen_item['price'] = all_list[4].xpath(".//td[2]/text()").extract_first().split(' ')[0]
            xiamen_item['area'] = all_list[5].xpath(".//td[2]/text()").extract_first().split(' ')[0]
            # xiamen_item['status'] = all_list[6].xpath(".//td[2]/text()").extract_first()
        except:
            print('=====')
            xiamen_item['address'] = all_list[0].xpath(".//td[2]/text()").extract_first()
            xiamen_item['room_id'] = all_list[1].xpath(".//td[2]/text()").extract_first()
            # xiamen_item['property'] = all_list[2].xpath(".//td[2]/text()").extract_first()
            xiamen_item['use'] = all_list[2].xpath(".//td[2]/text()").extract_first()
            xiamen_item['price'] = all_list[3].xpath(".//td[2]/text()").extract_first().split(' ')[0]
            # xiamen_item['area'] = all_list[5].xpath(".//td[2]/text()").extract_first().split(' ')[0]
            xiamen_item['status'] = all_list[4].xpath(".//td[2]/text()").extract_first()
        print(xiamen_item)
        yield xiamen_item
        # next_link = response.xpath("")
        # if next_link:
        #     next_link = next_link[0]
            # yield scrapy.Request("http://fdc.xmtfj.gov.cn:8001/Lp/LPPartial"+next_link, callback=self.parse)