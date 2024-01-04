import json
from fastapi.testclient import TestClient

from app.main import create_app
from app.mongodb import create_mongo_connection

client = TestClient(create_app())

def test_ping() -> None:
    response = client.get("/ping/hello")
    assert response.status_code == 200
    assert response.json() == {"ping_message": "hello"}

def test_mongo_conn() -> None:
    mongo_client = create_mongo_connection()
    try:
        ping_message = mongo_client.admin.command('ping') 
    except Exception as e:
        print(e)
        assert False

    assert ping_message == {'ok': 1.0}

    db_name = 'image'
    image_db = mongo_client[db_name]

    coll_name = 'logs'
    logs = image_db[coll_name]

    # check adding test doc in database
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    eg_document = {'timestamp':timestamp,
                   'img_url':'https://testurl.com',
                   'img_class':'None',
                   'img_pred_prob': float(0.0)}
    doc = logs.insert_one(eg_document)
    assert doc.acknowledged == True
    assert logs.find_one({'timestamp':timestamp}) == {'_id': doc.inserted_id,
                                                        'timestamp': timestamp,
                                                        'img_url': 'https://testurl.com',
                                                        'img_class': 'None',
                                                        'img_pred_prob': 0.0}

    # MongoDB does not create a database until a collection (table) is created with at least one document (record)
    assert db_name in mongo_client.list_database_names()
    assert coll_name in image_db.list_collection_names() 

def test_model_prediction() -> None:
    img_url = 'https://cdn2.momjunction.com/wp-content/uploads/2021/02/What-Is-A-Sigma-Male-And-Their-Common-Personality-Trait-624x702.jpg'
    data = {'img_url':img_url}
    content = json.dumps(data)
    headers = {"Content-Type": "application/json"}

    response = client.post(f"/classify/", content=content, headers=headers)

    assert response.status_code == 200 # since there is not database connected to store image data
    assert response.json() == {'img_url':img_url,
                               'img_class':"Male",
                               'img_pred_prob':float(0.9999271035194397),
                               'doc_status':'inserted'}