# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import time


#mySpider/settings.py 设置pipeline才能生效, mySpider/items.py定义item
class MyspiderPipeline:
    def process_item(self, item, spider):
        if len(item["title"])>0:
            try:
                fd = open("data/data.txt","a+")
                fd.write(item["title"].strip()+"\n\n")
                fd.write(item["article"].strip()+"\n\n\n\n")
                fd.close()

                todayFile = "data/cnn_"+time.strftime("%y%m%d", time.localtime())+".txt"
                todayFd = open(todayFile,"a+")
                todayFd.write(item["title"].strip()+"\n\n")
                todayFd.write(item["article"].strip()+"\n\n\n\n")
                todayFd.close()
            except Exception as e:
                print(e)

        return item
