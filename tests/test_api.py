import pytest

from fastapi.testclient import TestClient
from fastapi_pagination import add_pagination

from sqlalchemy.orm import Session


from scripts.app import app
add_pagination(app)

from data_models import Base, engine
from data_ingestion.create_tables import create_tables
from data_ingestion.ingest_weather_data import ingest_file
from data_analysis.aggregate_by_year import aggregate_by_year



# Pytest fixture for setting up the database
@pytest.fixture(scope='function')
def session():
    create_tables()
    filepath = 'data/wx_data/USC00110072.txt'
    ingest_file(filepath)
    aggregate_by_year()

    yield

    # Teardown: close the session and drop all tables
    Base.metadata.drop_all(engine)


test_client = TestClient(app)


def test_read_main():
    response = test_client.get("/")

    assert response.status_code == 200


def test_read_weather_data_with_date(session):
    response = test_client.get("/api/weather/?station_id=USC00110072&date=1993-09-14").json()

    assert response['items'][0]['max_temp'] == 222
    assert response['items'][0]['min_temp'] == 100
    assert response['items'][0]['precipitation'] == 183


def test_read_weather_data_without_date(session):
    response = test_client.get("/api/weather/?station_id=USC00110072").json()

    assert len(response['items']) == 50
    assert response['total'] == 10865
    assert response['items'][0]['date'] == '1985-01-01'
    assert response['items'][0]['max_temp'] == -22
    assert response['items'][0]['min_temp'] == -128
    assert response['items'][0]['precipitation'] == 94
    

def test_read_weather_data_stats_with_year(session):
    response = test_client.get("/api/weather/stats/?station_id=USC00110072&year=1991").json()

    assert response['items'][0]['year'] == 1991
    assert response['items'][0]['avg_max_temp'] == pytest.approx(16.415966386554622, rel=1e-3)
    assert response['items'][0]['avg_min_temp'] == pytest.approx(5.261299435028248, rel=1e-3)
    assert response['items'][0]['total_precipitation'] == pytest.approx(79.06, rel=1e-3)


def test_read_weather_data_stats_without_year(session):
    response = test_client.get("/api/weather/stats/?station_id=USC00110072").json()

    assert len(response['items']) == 30
    assert response['total'] == 30
    assert response['items'][0]['year'] == 1985
    assert response['items'][0]['avg_max_temp'] == pytest.approx(15.334794520547945, rel=1e-3)
    assert response['items'][0]['avg_min_temp'] == pytest.approx(4.3264462809917354, rel=1e-3)
    assert response['items'][0]['total_precipitation'] == pytest.approx(78.01, rel=1e-3)
