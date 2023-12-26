import requests
import random

def test_api():
    url = 'http://localhost:5000/api/location'

    # 基準值
    base_latitude = 37.4221
    base_longitude = -122.0841
    base_carbon_saved = 2.5

    # 生成隨機值
    latitude = base_latitude + random.uniform(-10, 10)
    longitude = base_longitude + random.uniform(-10, 10)
    carbon_saved = base_carbon_saved + random.uniform(-10, 10)

    data = {
        'latitude': latitude,
        'longitude': longitude,
        'carbonSaved': carbon_saved
    }

    response = requests.post(url, json=data)
    print(response.json())

if __name__ == "__main__":
    test_api()
