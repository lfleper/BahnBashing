import pymongo

from bahn_bashing import settings
from scrapy.exceptions import DropItem


class MongoPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_server=crawler.settings.get('MONGODB_SERVER'),
            mongo_port=crawler.settings.get('MONGODB_PORT'),
            mongo_db=crawler.settings.get('MONGODB_DB'),
            mongo_collection=crawler.settings.get('MONGODB_COLLECTION')
        )

    def __init__(self, mongo_server, mongo_port, mongo_db, mongo_collection):
        connection = pymongo.MongoClient(
            mongo_server,
            mongo_port
        )
        db = connection[mongo_db]
        self.collection = db[mongo_collection]

    def process_item(self, item, spider):
        for data in item:
            if not data:
                raise DropItem("Missing data!")
        self.collection.insert(item)
        return item
