from datetime import date

import pytest

from sqlalchemy import inspect
from sqlalchemy.orm import Session

from data_models import Base, engine
from data_models.weather_data import WeatherData
from data_ingestion.create_tables import create_tables
from data_ingestion.ingest_weather_data import ingest_file


# Pytest fixture for setting up the database
@pytest.fixture(scope='function')
def session():
    create_tables()

    session = Session(engine)
    yield session

    # Teardown: close the session and drop all tables
    session.close()
    Base.metadata.drop_all(engine)


def test_table_created(session):
    inspector = inspect(session.bind)
    tables = inspector.get_table_names()

    assert 'weather_data' in tables


def test_columns_exist(session):
    inspector = inspect(session.bind)
    columns = inspector.get_columns('weather_data')

    column_names = [column['name'] for column in columns]

    assert 'station_id' in column_names
    assert 'date'       in column_names
    assert 'max_temp'   in column_names
    assert 'min_temp'   in column_names


def test_insert_data(session):
    filepath = 'data/wx_data/USC00110072.txt'

    with open(filepath, 'r') as file:
        line_count = sum(1 for line in file)

    ingest_file(filepath)

    result = session.query(WeatherData).all()
    assert result is not None

    # Validate values from one of the rows
    assert result[180].date == date(year=1985, month=6, day=30)
    assert result[180].max_temp == 294
    assert result[180].min_temp == 156
    assert result[180].precipitation == 0
    
    # Validate the -9999s are parsed correctly as NaNs
    assert result[31].min_temp is None
    
    # Validate number of rows inserted is correct
    assert len(result) == line_count
