from datetime import date

import pytest

from sqlalchemy.orm import Session

from data_models import Base, engine
from data_models.yearly_aggregations import YearlyAggregation
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


def test_insert_data(session):
    aggregate_by_year()

    result = session.query(YearlyAggregation).all()
    assert result is not None

    assert len(result) == 30

    # Check the results for one particular year
    assert result[3].year == 1988
    assert result[3].avg_max_temp == pytest.approx(17.347267759562843, rel=1e-3)
    assert result[3].avg_min_temp == pytest.approx(4.534972677595628, rel=1e-3)
    assert result[3].total_precipitation == pytest.approx(54.1, rel=1e-3)
