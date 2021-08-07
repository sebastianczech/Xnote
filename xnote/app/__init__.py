import xnote.settings

from pymongo import MongoClient

mongoClient = MongoClient(xnote.settings.MONGO_DB_URI)
mongoDatabase = mongoClient.sebastianczech
