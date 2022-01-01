ITEM_PIPELINES = {
    'bahn_bashing.mongo.connection.MongoPipeline': 1
}

DOWNLOADER_MIDDLEWARES = {
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
}

ROTATING_PROXY_LIST_PATH = './http_proxies.txt'

BOT_NAME = 'bahn_bashing'

SPIDER_MODULES = ['bahn_bashing.spider']
NEWSPIDER_MODULE = 'bahn_bashing.spider'

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "bahn_bashing"
MONGODB_COLLECTION = "routes"

CONCURRENT_REQUESTS_PER_DOMAIN = 48
CONCURRENT_REQUESTS = 48
#DOWNLOAD_DELAY = 2
DOWNLOAD_TIMEOUT = 240

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64)"
