from fastapi.testclient import TestClient
# pip install httpx2
#nose2 --with-coverage
from app.main import app

client = TestClient(app)


def test_eligibility_pass():
    payload = {
        'income': 60000,
        'age': 25,
        'employment_status': 'employed'
    }
    response = client.post('/loan-eligibility', json=payload)
    assert response.status_code == 200
    assert response.json() == {'eligible': True}


def test_eligibility_fail():
    payload = {
        'income': 30000,
        'age': 18,
        'employment_status': 'unemployed'
    }
    response = client.post('/loan-eligibility', json=payload)
    assert response.status_code == 200
    assert response.json() == {'eligible': False}