ITEM_PIPELINES = {
    'bahn_bashing.mongo.connection.MongoPipeline': 1
}

BOT_NAME = 'bahn_bashing'

SPIDER_MODULES = ['bahn_bashing.spider']
NEWSPIDER_MODULE = 'bahn_bashing.spider'

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "bahn_bashing"
MONGODB_COLLECTION = "routes"
DOWNLOAD_DELAY = 8
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64)"
