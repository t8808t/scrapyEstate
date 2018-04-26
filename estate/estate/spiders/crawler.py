from scrapy import Request
from scrapy.spiders import Spider
from estate.items import EstateItem
import json
import re
import requests
class EstateSpider(Spider):
    name = 'estate'

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        base_urls = 'YourURL'
        response = requests.get(base_urls,headers =headers)
        respList = json.loads(response.text)
        reobj_Page = re.compile('href="javascript:void\(0\)" class="c" onclick="doPage\((\d+)\);return false;')  # 正则匹配出当前页码和总页码
        totalPage = reobj_Page.findall(respList['pageinfo'])[1]
        print("totalPage : "+totalPage)
        for nextPage in range(1, int(totalPage)):
            absolute_next_page_url =  'YourURL?page='+str(nextPage)
            yield Request(absolute_next_page_url, self.parse)

    def parse(self, response):
        item = EstateItem()
        respList = json.loads(response.body)
        jsobjs = respList['list']
        for jsobj in jsobjs:
            item["cjsj"] = jsobj['cjsj']
            item["scgpshsj"] = jsobj['scgpshsj']
            item["fwtybh"] = jsobj['fwtybh']
            item["fczsh"] = jsobj['fczsh']
            item["gplxrxm"] = jsobj['gplxrxm']
            item["mdmc"] = jsobj['mdmc']
            item["cqmc"] = jsobj['cqmc']
            item["xzqhname"] = jsobj['xzqhname']
            item["xqmc"] = jsobj['xqmc']
            item["jzmj"] = jsobj['jzmj']
            item["wtcsjg"] = jsobj['wtcsjg']
            yield item

        reobj_Page = re.compile('href="javascript:void\(0\)" class="c" onclick="doPage\((\d+)\);return false;') # 正则匹配出当前页码和总页码
        nextPage = reobj_Page.findall(respList['pageinfo'])[0]
        #currentPage = int(nextPage) - 1
        totalPage1 = reobj_Page.findall(respList['pageinfo'])[1]
        #print("当前页码为 : "+ str(currentPage))
        print(nextPage + " / " + totalPage1)
