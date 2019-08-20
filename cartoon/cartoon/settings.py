# -*- coding: utf-8 -*-

# Scrapy settings for cartoon project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

# 爬虫名称
BOT_NAME = 'cartoon'

# 爬虫应用路径
SPIDER_MODULES = ['cartoon.spiders']
NEWSPIDER_MODULE = 'cartoon.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# 客户端user-agent请求头
#USER_AGENT = 'cartoon (+http://www.yourdomain.com)'

# Obey robots.txt rules
# 禁止爬虫配置
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# 并发请求数
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# 延迟下载秒数
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# 单域名访问并发数，并且延迟下次秒数也应用在每个域名
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
# 单IP访问并发数，如果有值则忽略：CONCURRENT_REQUESTS_PER_DOMAIN，并且延迟下次秒数也应用在每个IP
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# 是否支持cookie，cookiejar进行操作cookie
#COOKIES_ENABLED = True
#COOKIES_DEBUG = True

# Disable Telnet Console (enabled by default)
# Telnet用于查看当前爬虫的信息，操作爬虫等...
# 使用telnet ip port ，然后通过命令操作
#TELNETCONSOLE_ENABLED = True
#TELNETCONSOLE_HOST = '127.0.0.1'
#TELNETCONSOLE_PORT = [6023,]

# Override the default request headers:
# 默认请求头
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   'cartoon.middlewares.CartoonSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'cartoon.middlewares.CartoonDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# 自定义扩展，基于信号进行调用
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# 定义pipeline处理请求
ITEM_PIPELINES = {
   'cartoon.pipelines.W3SchoolPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# 开始自动限速
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
# 初始下载延迟
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# 最大下载延迟
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# 平均每秒并发数
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# 调试
#AUTOTHROTTLE_DEBUG = False

# 爬虫允许的最大深度，可以通过meta查看当前深度；0表示无深度
# DEPTH_LIMIT = 3

# 爬取时，0表示深度优先Lifo(默认)；1表示广度优先FiFo

# 后进先出，深度优先
# DEPTH_PRIORITY = 0
# SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleLifoDiskQueue'
# SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.LifoMemoryQueue'

# 先进先出，广度优先
# DEPTH_PRIORITY = 1
# SCHEDULER_DISK_QUEUE = 'scrapy.squeue.PickleFifoDiskQueue'
# SCHEDULER_MEMORY_QUEUE = 'scrapy.squeue.FifoMemoryQueue'

# 调度器队列
# SCHEDULER = 'scrapy.core.scheduler.Scheduler'
# from scrapy.core.scheduler import Scheduler

# 访问URL去重
# DUPEFILTER_CLASS = 'step8_king.duplication.RepeatUrl'

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# 是否启用缓存策略
#HTTPCACHE_ENABLED = True

# 缓存策略：所有请求均缓存，下次在请求直接访问原来的缓存即可
# HTTPCACHE_POLICY = "scrapy.extensions.httpcache.DummyPolicy"
# 缓存策略：根据Http响应头：Cache-Control、Last-Modified 等进行缓存的策略
# HTTPCACHE_POLICY = "scrapy.extensions.httpcache.RFC2616Policy"

# 缓存超时时间
#HTTPCACHE_EXPIRATION_SECS = 0
# 缓存保存路径
#HTTPCACHE_DIR = 'httpcache'
# 缓存忽略的Http状态码
#HTTPCACHE_IGNORE_HTTP_CODES = []
# 缓存存储的插件
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
