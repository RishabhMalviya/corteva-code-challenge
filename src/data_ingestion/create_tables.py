from data_models import Base
from data_models import engine
from data_models.weather_data import WeatherData
from data_models.yearly_aggregations import YearlyAggregation


def create_tables():
    Base.metadata.create_all(engine)
