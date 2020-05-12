from  scrapy import cmdline
# 输出未过滤的页面信息
cmdline.execute('scrapy crawl douban_spider'.split())

# 抓取目标:
# 本文通过网页豆瓣电影排行数据的抓取和清洗
# https://movie.douban.com/top250列表