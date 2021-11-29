import json
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_index():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'This is a test message'}

def test_calculateOverweight():
    response = client.post(
        '/calculateOverweight',
        json = [{"Gender": "Female", "HeightCm": 167, "WeightKg": 82}, {"Gender": "Male", "HeightCm": 172, "WeightKg": 88}],
        )
    assert response.status_code == 200
    assert response.json() == [{'Count of Overweight users': 2}]

def test_calculateOverweight_zeroheight():
    response = client.post(
        '/calculateOverweight',
        json = [{"Gender": "Female", "HeightCm": 0, "WeightKg": 82}],
        )
    assert response.status_code == 500
    #assert response.json() == {"detail": "Error while calculating Overweight.. Error message : string indices must be integers"}

def test_calculateOverweight_zeroweight():
    response = client.post(
        '/calculateOverweight',
        json = [{"Gender": "Female", "HeightCm": 170, "WeightKg": 0}],
        )
    assert response.status_code == 200
    assert response.json() == [{'Count of Overweight users': 0}]

def test_calculateOverweight_heightString():
    response = client.post(
        '/calculateOverweight',
        json = [{"Gender": "Female", "HeightCm": 'abg', "WeightKg": 82}],
        )
    assert response.status_code == 422

def test_calculateBMI():
    response = client.post(
        '/calculateBMI',
        json = [{"Gender": "Male", "HeightCm": 170, "WeightKg": 96 }, { "Gender": "Male", "HeightCm": 161, "WeightKg": 85 }]
        )
    assert response.status_code == 200
    assert response.json() == [{"Gender": "Male", "HeightCm": 170, "WeightKg": 96, "BMICategory": "Moderately obese", "HealthRisk": "Medium risk"},
                                {"Gender": "Male", "HeightCm": 161, "WeightKg": 85, "BMICategory": "Moderately obese", "HealthRisk": "Medium risk"}] 


def test_calculateBMI_zeroheight():
    response = client.post(
        '/calculateBMI',
        json = [{"Gender": "Male", "HeightCm": 0, "WeightKg": 96 }]
        )
    assert response.status_code == 500

def test_calculateBMI_heightString():
    response = client.post(
        '/calculateBMI',
        json = [{"Gender": "Male", "HeightCm": 'abcv', "WeightKg": 96 }]
        )
    assert response.status_code == 422

def test_calculateBMI_weightString():
    response = client.post(
        '/calculateBMI',
        json = [{"Gender": "Male", "HeightCm": 175, "WeightKg": 'abcv' }]
        )
    assert response.status_code == 422


