import scrapy
import os,hashlib,json
from lxml import etree
from mySpider.items import MyspiderItem

class CnnSpider(scrapy.Spider):
    name = 'cnn'
    allowed_domains = ['edition.cnn.com']
    start_urls = ['https://edition.cnn.com/business',"https://edition.cnn.com/business/tech","https://edition.cnn.com/business/investing"]
    #没有返回列表
    #start_urls = ["https://edition.cnn.com/business/tech", "https://edition.cnn.com/business/economy", "https://edition.cnn.com/business/energy"]

    def parse(self, response):
        try:
            #选取所有 h3 元素，且这些元素拥有值为 cd__headline 的 class 属性。
            path = '//h3[@class="cd__headline"]'
            rsp = response.xpath(path)
            print("size:",len(rsp))
            difffile = "data/diff.json"
            diffJson = {}
            if os.path.exists(difffile):
                rfd_diff = open(difffile,"r", encoding="utf8")
                content = rfd_diff.read()
                #print("read content:", content)
                if content!="":
                    diffJson = json.loads(content)
                rfd_diff.close()
            #print("==========",diffJson)

            hl = hashlib.md5()
            for item in rsp:
                link = item.xpath('./a/@href').extract()
                title = item.xpath('./a/span/text()').extract()
                hl.update(title[0].encode(encoding="utf8"))
                diffKey = hl.hexdigest()
                if diffKey in diffJson:
                    continue
                diffJson[diffKey] = 1
                geturl = "https://edition.cnn.com"+link[0]
                yield scrapy.Request(geturl,callback=self.myparse)
            diffStr = json.dumps(diffJson)
            #print("diffStr:",diffStr)
            if diffStr!="":
                wfd_diff = open(difffile,"w+", encoding="utf8")
                wfd_diff.write(diffStr)
                wfd_diff.close()
        except Exception as e:
            print("Exception:",e)

    def myparse(self, response):
        #/text()将选择器的内容作为data
        path = '//h1[@class="pg-headline"]/text()'
        #extract提取data
        title = ""
        rsp = response.xpath(path).extract()
        if len(rsp)>0:
            title = rsp[0]
        print("title:", title)
        
        sentencesList = []
        path = '//p[@class="zn-body__paragraph speakable"]'
        sentences = response.xpath(path)
        for sentence in sentences:
            #提取改标签下所有文本内容，包括该标签下的a标签
            sentenceStr = sentence.xpath('string(.)').extract()
            sentencesList.append(" ".join(list(map(lambda x:x.strip(), sentenceStr))))

        path = '//div[@class="zn-body__paragraph"]'
        sentences = response.xpath(path)
        for sentence in sentences:
            sentenceStr = sentence.xpath('string(.)').extract()
            sentencesList.append(" ".join(list(map(lambda x:x.strip(), sentenceStr))))

        article = "\n".join(list(filter(lambda x:len(x)>0, sentencesList)))
        item = MyspiderItem()
        item["title"] = title
        item["article"] = article
        yield item



