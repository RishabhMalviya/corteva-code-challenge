from datetime import date

import pytest

from sqlalchemy import inspect
from sqlalchemy.orm import Session

from data_models import Base
from data_models import engine
from data_ingestion.create_tables import create_tables
from data_ingestion.ingest_weather_data import ingest_file
from data_analysis.aggregate_by_year import aggregate_by_year


# Pytest fixture for setting up the database
@pytest.fixture(scope='function')
def session():
    create_tables()
    filepath = 'data/wx_data/USC00110072.txt'
    ingest_file(filepath)
    session = Session(engine)

    yield session

    # Teardown: close the session and drop all tables
    session.close()
    Base.metadata.drop_all(engine)


def test_table_created(session):
    inspector = inspect(session.bind)
    tables = inspector.get_table_names()

    assert 'weather_data' in tables

def test_insert_data(session):
    aggregate_by_year()
