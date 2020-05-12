# -*- coding: utf-8 -*-
import scrapy
from ..items import DoubanItem
class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫的名称
    name = 'douban_spider'
    # 爬虫允许抓取的域名
    allowed_domains = ['movie.douban.com']
    # 爬虫抓取数据地址,给调度器
    start_urls = ['http://movie.douban.com/top250']

    def parse(self, response):
        # 获取电影列表
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        for i_item in movie_list:
            # 初始化模型
            douban_item = DoubanItem()
            # 获取电影的信息，赋值给模型各字段，一一对应
            douban_item['serial_number'] = i_item.xpath(".//div[@class='item']//em/text()").extract_first()
            douban_item['movie_name'] = i_item.xpath(".//div[@class='item']//span[@class='title']/text()").extract_first()
            descs = i_item.xpath(".//div[@class='info']//div[@class='bd']/p[1]/text()").extract()
            for i_desc in descs:
                i_desc_str = "".join(i_desc.split( ))
                douban_item['introduce'] = i_desc_str
            douban_item['star'] = i_item.xpath(".//div[@class='star']//*[@class='rating_num']/text()").extract_first()
            douban_item['evaluate'] = i_item.xpath(".//div[@class='star']//span[4]/text()").extract_first()
            douban_item['describle'] = i_item.xpath(".//p[@class='quote']/span/text()").extract_first()
            yield douban_item
        # 解析下一页
        next_link = response.xpath("//span[@class='next']/link/@href").extract()
        if next_link:
            next_link = next_link[0]
            # 下一页链接
            next_url="https://movie.douban.com/top250" + next_link
            yield scrapy.Request(next_url,callback=self.parse)

