import requests
from datetime import datetime, timedelta
from uuid import UUID

# Define the base URL of your FastAPI server
BASE_URL = "http://localhost:8000"


def test_hello_endpoint():
    # Make a GET request to the endpoint
    response = requests.get(BASE_URL + "/")

    # Assert that the status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response contains the expected message
    expected_message = {"message": "Hello, FastAPI!"}
    assert response.json() == expected_message


def test_get_table_name_not_found():
    url = BASE_URL + "/api/v1/user/test"

    response = requests.get(url)

    assert response.status_code == 400


def test_get_table_name_single():
    url = BASE_URL + "/api/v1/user/Michael"

    response = requests.get(url)

    assert response.status_code == 200


def test_get_table_multiple():
    url = BASE_URL + "/api/v1/search/restaurants"
    eaters = ["Michael", "Lucile", "Gob", "Maeby"]
    eater_ids = []
    for eater in eaters:
        eater_url = BASE_URL + f"/api/v1/user/{eater}"
        response = requests.get(eater_url)
        json_response = response.json()
        eater_ids.append(json_response["id"])
    params = {"eaters": eater_ids, "time": datetime.now().isoformat()}
    response = requests.get(url, params=params)

    results = response.json()

    assert response.status_code == 200
    assert results == None


def test_get_table():
    url = BASE_URL + "/api/v1/search/restaurants"
    eaters = ["Michael"]
    eater_ids = []
    for eater in eaters:
        eater_url = BASE_URL + f"/api/v1/user/{eater}"
        response = requests.get(eater_url)
        json_response = response.json()
        eater_ids.append(json_response["id"])
    params = {"eaters": eater_ids, "time": datetime.now().isoformat()}
    response = requests.get(url, params=params)

    expected_names = set(["u.to.pi.a", "Panadería Rosetta"])

    results = response.json()
    result_names = set([result["name"] for result in results])

    assert response.status_code == 200
    assert result_names == expected_names


def test_get_table_multiple_2():
    url = BASE_URL + "/api/v1/search/restaurants"
    eaters = ["Michael", "George Michael"]
    eater_ids = []
    for eater in eaters:
        eater_url = BASE_URL + f"/api/v1/user/{eater}"
        response = requests.get(eater_url)
        json_response = response.json()
        eater_ids.append(json_response["id"])
    params = {"eaters": eater_ids, "time": datetime.now().isoformat()}
    response = requests.get(url, params=params)

    expected_names = set(["Panadería Rosetta"])

    results = response.json()
    result_names = set([result["name"] for result in results])

    assert response.status_code == 200
    assert result_names == expected_names


def test_book_reseration():
    search_url = BASE_URL + "/api/v1/search/restaurants"
    eaters = ["Michael"]
    time = datetime.now()
    eater_ids = []
    for eater in eaters:
        eater_url = BASE_URL + f"/api/v1/user/{eater}"
        response = requests.get(eater_url)
        json_response = response.json()
        eater_ids.append(json_response["id"])
    params = {"eaters": eater_ids, "time": datetime.now().isoformat()}

    # Search for available restaurants
    response = requests.get(search_url, params=params)

    results = response.json()

    reseravation_url = BASE_URL + "/api/v1/reservation"
    reservation_data = {
        "restaurant_id": results[0]["id"],
        "created_at": time.isoformat(),
        "eaters": eaters,
    }

    # Create a reservation
    response = requests.post(reseravation_url, json={**reservation_data})

    assert response.status_code == 200

    # Delete the reservation
    delete_response = requests.delete(reseravation_url + f"/{response.json()['id']}")
    assert delete_response.status_code == 200

    # 2 reservation with the same time should failed
    response = requests.post(reseravation_url, json={**reservation_data})
    second_response = requests.post(reseravation_url, json={**reservation_data})
    response_json = second_response.json()
    assert second_response.status_code == 400
    assert response_json["detail"] == "ExistingReservationDuringTimeFrame"

    # create reservation until out of tables
    third_response = requests.post(
        reseravation_url,
        json={
            **{
                "restaurant_id": results[0]["id"],
                "created_at": (time + timedelta(hours=5)).isoformat(),
                "eaters": eaters,
            }
        },
    )

    assert third_response.status_code == 200
    new_time = time + timedelta(hours=10)
    while True:
        new_time = new_time + timedelta(hours=5)

        fourth_response = requests.post(
            reseravation_url,
            json={
                **{
                    "restaurant_id": results[0]["id"],
                    "created_at": new_time.isoformat(),
                    "eaters": eaters,
                }
            },
        )
        if fourth_response.status_code == 400:
            fourth_response_json = fourth_response.json()
            assert fourth_response_json["detail"] == "RestaurantCantFulfillReservation"
            break
