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

def test_retrieve_prediction() ->None:
    img_url = 'https://test.com'
    model = 'gender-classifier'
    response = client.get(f'/results/?model={model}&img_url={img_url}')

    assert response.status_code == 200 
    assert response.json() == {"status": "Doc not found"}

def test_gender_prediction() -> None:
    img_url = 'https://upload.wikimedia.org/wikipedia/commons/1/1b/Ex_-_L_-_low_quality.jpg'
    data = {'img_url':img_url}
    content = json.dumps(data)
    headers = {"Content-Type": "application/json"}

    response = client.post(f"/classify/gender/", content=content, headers=headers)

    assert response.status_code == 201 #doc should be inserted

    # since model predcits different probability scores, only url checks is made
    assert response.json()['img_url'] == img_url
    assert response.json()['img_class'] == "Male"
    assert response.json()['model'] == "gender-classifier"
                            
def test_digit_prediction() -> None:
    img_url = 'https://i.stack.imgur.com/RdEpj.png'
    data = {'img_url':img_url}
    content = json.dumps(data)
    headers = {"Content-Type": "application/json"}

    response = client.post(f"/classify/digit/", content=content, headers=headers)

    assert response.status_code == 201 #doc should be inserted

    # since model predcits different probability scores, only url checks is made
    assert response.json()['img_url'] == img_url
    assert response.json()['img_class'] == str(6)
    assert response.json()['model'] == "digit-classifier"