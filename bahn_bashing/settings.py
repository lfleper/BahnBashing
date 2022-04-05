import requests

ITEM_PIPELINES = {
    'bahn_bashing.mongo.connection.MongoPipeline': 1
}

DOWNLOADER_MIDDLEWARES = {
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
}

BOT_NAME = 'bahn_bashing'

SPIDER_MODULES = ['bahn_bashing.spider']
NEWSPIDER_MODULE = 'bahn_bashing.spider'

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "bahn_bashing"
MONGODB_COLLECTION = "routes"

CONCURRENT_REQUESTS_PER_DOMAIN = 40
CONCURRENT_REQUESTS = 40
DOWNLOAD_DELAY = 0
DOWNLOAD_TIMEOUT = 30

ROTATING_PROXY_PAGE_RETRY_TIMES = 100


def get_proxies(proxy_endpoint):
    r = requests.get(proxy_endpoint)
    proxies = r.text.split("\n")
    proxies = [x for x in proxies if x]
    print("Proxies:", proxies)
    return proxies


ROTATING_PROXY_LIST = get_proxies("https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt")

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64)"
