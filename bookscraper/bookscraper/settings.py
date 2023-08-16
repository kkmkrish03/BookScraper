# Scrapy settings for bookscraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "bookscraper"

SPIDER_MODULES = ["bookscraper.spiders"]
NEWSPIDER_MODULE = "bookscraper.spiders"

FEEDS = {
   'booksdata.json': {'format': 'json'}
}
# MY SQL config
SQL_HOST = 'localhost'
SQL_USER = 'root'
SQL_PASSWORD =''
SQL_DATABASE = 'scraper'
SQL_ENABLED = True

SCRAPEOPS_API_KEY = ''
SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT = 'https://headers.scrapeops.io/v1/user-agents'
SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT = 'https://headers.scrapeops.io/v1/browser-headers'
SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED = True
SCRAPEOPS_FAKE_USER_AGENT_ENABLED = True
SCRAPEOPS_NUM_RESULTS = 50

# (proxy_method_2)
# Get from https://geonode.com/free-proxy-list or https://free-proxy-list.net/
ROTATING_PROXY_LIST = {
   '106.75.154.243:999',
   '197.234.13.52:4145',
   '104.16.25.216:80',
   '82.202.196.126:9050',
   '209.141.47.74:1337',
   '64.225.8.115:9996'
}
# ROTATING_PROXY_LIST_PATH = './proxy-list.txt'
# (proxy_method_2.1)
PROXYLIST_ENABLED = False
PROXYLIST_BY = 'SPEED' #SPEED, UPTIME, RESPONSE
PROXYLIST_LIMIT = '10'
ROTATING_PROXYLIST_ENDPOINT_BY_UP_TIME = f'https://proxylist.geonode.com/api/proxy-list?limit={PROXYLIST_LIMIT}&page=1&sort_by=upTime&sort_type=desc'
ROTATING_PROXYLIST_ENDPOINT_BY_SPEED = f'https://proxylist.geonode.com/api/proxy-list?limit={PROXYLIST_LIMIT}&page=1&sort_by=speed&sort_type=asc'
ROTATING_PROXYLIST_ENDPOINT_BY_RESPONSE = f'https://proxylist.geonode.com/api/proxy-list?limit={PROXYLIST_LIMIT}&page=1&sort_by=responseTime&sort_type=asc'


# (proxy_method_3)
# Premium proxy
PROXY_USER = ''
PROXY_PASSWORD = ''
PROXY_ENDPOINT = 'gate.smartproxy.com'
PROXY_PORT = '7000'

# (proxy_method_4)
SCRAPEOPS_API_KEY = ''
SCRAPEOPS_PROXY_ENABLED = True
SCRAPEOPS_PROXY_SETTINGS = {'country': 'us'}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "bookscraper (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "bookscraper.middlewares.BookscraperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   "bookscraper.middlewares.BookscraperDownloaderMiddleware": 543,
   "bookscraper.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware": 400,
   # (proxy_method_2)
   # "rotating_proxies.middlewares.RotatingProxyMiddleware": 610,
   # "rotating_proxies.middlewares.BanDetectionMiddleware": 620,
   # (proxy_method_2.1)
   "bookscraper.middlewares.MyFreeProxyMiddleware": 630,
   # (proxy_method_3)
   # "bookscraper.middlewares.MyProxyMiddleware": 350,
   # (proxy_method_4)
   # "scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk": 725,

}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "bookscraper.pipelines.BookscraperPipeline": 300,
   "bookscraper.pipelines.SaveToMySQLPipeline": 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
