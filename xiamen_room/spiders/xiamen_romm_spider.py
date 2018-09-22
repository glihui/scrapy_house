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
                'BuildID': '6000024846',
                'NAID': '29406',
                'lotid': '123684',
                't': '1537614049842'
            },
            {
                'BuildID': '6000024842',
                'NAID': '29405',
                'lotid': '123684',
                't': '1537614182877'
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
            for item_value in all_list:
                tmp_value = item_value.xpath(".//td[1]/text()").extract_first()
                tmp_value_2 = item_value.xpath(".//td[2]/text()").extract_first()
                if tmp_value == '坐落':
                    xiamen_item['address'] = tmp_value_2
                elif tmp_value == '室号':
                    xiamen_item['room_id'] = tmp_value_2
                elif tmp_value == '性质':
                    xiamen_item['property'] = tmp_value_2
                elif tmp_value == '用途':
                    xiamen_item['use'] = tmp_value_2
                elif tmp_value == '面积':
                    xiamen_item['area'] = tmp_value_2.split(' ')[0]
                elif tmp_value == '拟售价格':
                    xiamen_item['price'] = tmp_value_2.split(' ')[0]
                elif tmp_value == '权属状态':
                    xiamen_item['status'] = tmp_value_2


            # xiamen_item['address'] = all_list[0].xpath(".//td[2]/text()").extract_first()
            # xiamen_item['room_id'] = all_list[1].xpath(".//td[2]/text()").extract_first()
            # xiamen_item['property'] = all_list[2].xpath(".//td[2]/text()").extract_first()
            # xiamen_item['use'] = all_list[3].xpath(".//td[2]/text()").extract_first()
            # xiamen_item['price'] = all_list[4].xpath(".//td[2]/text()").extract_first().split(' ')[0]
            # xiamen_item['area'] = all_list[5].xpath(".//td[2]/text()").extract_first().split(' ')[0]
            # xiamen_item['status'] = all_list[6].xpath(".//td[2]/text()").extract_first()
        except:
            pass
            # print('=====')
            # xiamen_item['address'] = all_list[0].xpath(".//td[2]/text()").extract_first()
            # xiamen_item['room_id'] = all_list[1].xpath(".//td[2]/text()").extract_first()
            # xiamen_item['property'] = all_list[2].xpath(".//td[2]/text()").extract_first()
            # xiamen_item['use'] = all_list[2].xpath(".//td[2]/text()").extract_first()
            # xiamen_item['price'] = all_list[3].xpath(".//td[2]/text()").extract_first().split(' ')[0]
            # xiamen_item['area'] = all_list[5].xpath(".//td[2]/text()").extract_first().split(' ')[0]
            # xiamen_item['status'] = all_list[4].xpath(".//td[2]/text()").extract_first()
        # print(xiamen_item)
        yield xiamen_item
        # next_link = response.xpath("")
        # if next_link:
        #     next_link = next_link[0]
            # yield scrapy.Request("http://fdc.xmtfj.gov.cn:8001/Lp/LPPartial"+next_link, callback=self.parse)