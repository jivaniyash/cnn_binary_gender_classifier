import pymongo

def create_mongo_connection() -> pymongo.MongoClient:
    # MongoDB connection details
    host = 'mongo_db' # container name
    port = 27017
    username = 'username'
    password = 'password'

    # Create a MongoClient
    mongo_client = pymongo.MongoClient(host=host, 
                                    port=port,
                                    username=username,
                                    password=password)
    
    return mongo_client

def insert_one_doc(img_url:str, img_class:str, prob:float):

    mongo_client = create_mongo_connection()

    db_name = 'image'
    coll_name = 'logs'

    if db_name not in mongo_client.list_database_names():
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

    return doc.acknowledged




