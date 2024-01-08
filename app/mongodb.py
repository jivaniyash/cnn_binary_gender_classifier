import pymongo
from app.settings import MongoDBConnectionSettings

def create_mongo_connection() -> pymongo.MongoClient:
    mongo_connection = MongoDBConnectionSettings()

    # Create a MongoClient
    mongo_client = pymongo.MongoClient(host=mongo_connection.host, 
                                    port=mongo_connection.port,
                                    username=mongo_connection.username,
                                    password=mongo_connection.password)
    
    return mongo_client

def insert_one_doc(img_url:str, img_class:str, prob:float):

    mongo_client = create_mongo_connection()

    db_name = 'image'
    coll_name = 'logs'

    if db_name not in mongo_client.list_database_names(): # create db & collection
        image_db = mongo_client[db_name]
        coll = image_db[coll_name]
    else:
        db = mongo_client.image
        coll = db.logs

    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    document = {'timestamp':timestamp,
                'img_url':img_url,
                'img_class':img_class,
                'img_pred_prob': prob}
    
    doc = coll.insert_one(document)
    if doc.acknowledged: # add doc_status key
        coll.update_one(filter={'img_url':img_url},update={'$set':{'doc_status':'inserted'}})
    return document

def find_doc(img_url: str):

    mongo_client = create_mongo_connection()

    db_name = 'image'
    coll_name = 'logs'

    if db_name not in mongo_client.list_database_names(): # create db & collection
        image_db = mongo_client[db_name]
        coll = image_db[coll_name]
    else:
        db = mongo_client.image
        coll = db.logs

    doc = coll.find_one({'img_url':img_url})

    if doc:
        return True, doc
    else:
        return False, None

