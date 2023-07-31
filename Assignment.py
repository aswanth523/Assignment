import requests
import pytest
from datetime import datetime, timedelta


def test_valid_request():
    """
    Test to check hours left for next birthday
    :return:
    """
    response = requests.get(
        "https://lx8ssktxx9.execute-api.eu-west-1.amazonaws.com/Prod/next-birthday?dateofbirth=1990-10-30&unit=hour")
    assert response.status_code == 200
    print(f"Check hours left for next birthday = {response.json()['message']}")
    assert response.json()["message"] == "2184 hours left"


def test_invalid_date_of_birth():
    """
    Test to check invalid date of birth
    :return:
    """
    response = requests.get(
        "https://lx8ssktxx9.execute-api.eu-west-1.amazonaws.com/Prod/next-birthday?dateofbirth=2023-02-30&unit=hour")
    # There is a bug url it is giving 200 as status code for feb 30 date
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid date of birth"


def test_invalid_unit():
    """
    Test to check invalid unit as year
    :return:
    """
    response = requests.get(
        "https://lx8ssktxx9.execute-api.eu-west-1.amazonaws.com/Prod/next-birthday?dateofbirth=1990-10-30&unit=year")
    # There is a bug url it is giving 200 as status code for unit as year
    assert response.status_code == 400
    assert response.json()["message"] == "Invalid unit"


def test_edge_cases():
    """
    Test cases with different date ranges current and previous date ranges
    :return:
    """
    current_date = datetime.now().strftime("%Y-%m-%d")
    response = requests.get(
        f"https://lx8ssktxx9.execute-api.eu-west-1.amazonaws.com/Prod/next-birthday?dateofbirth={current_date}&unit=day")
    assert response.status_code == 200
    assert response.json()["message"] == "0 days left"

    previous_date = (datetime.strptime(datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d") - timedelta(days=25)).strftime(
        "%Y-%m-%d")
    response = requests.get(
        f"https://lx8ssktxx9.execute-api.eu-west-1.amazonaws.com/Prod/next-birthday?dateofbirth={previous_date}&unit=day")
    assert response.status_code == 200
    assert response.json()["message"] == "341 days left"


def test_multiple_requests():
    """Test that multiple requests """
    for i in range(10):
        response = requests.get(
            "https://lx8ssktxx9.execute-api.eu-west-1.amazonaws.com/Prod/next-birthday?dateofbirth=1990-10-30&unit=hour")
        assert response.status_code == 200
        assert response.json()["message"] == "2184 hours left"
