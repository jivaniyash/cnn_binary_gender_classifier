import json
from fastapi.testclient import TestClient

from app.main import create_app

client = TestClient(create_app())

def test_ping() -> None:
    response = client.get("/ping/hello")
    assert response.status_code == 200
    assert response.json() == {"ping_message": "hello"}

def test_model_prediction() -> None:
    img_url = 'https://cdn2.momjunction.com/wp-content/uploads/2021/02/What-Is-A-Sigma-Male-And-Their-Common-Personality-Trait-624x702.jpg'
    data = {'img_url':img_url}
    content = json.dumps(data)
    headers = {"Content-Type": "application/json"}

    response = client.post(f"/classify/", content=content, headers=headers)
    assert response.status_code == 200 # since there is not database connected to store image data
    assert response.json() == {'img_url':img_url,
                               'img_class':"Male",
                               'img_pred_prob':float(0.9912407398223877)}