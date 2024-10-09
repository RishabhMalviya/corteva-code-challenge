import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
import coloredlogs

from sqlalchemy.orm import Session
from sqlalchemy import func

from data_models.weather_data import WeatherData
from data_models.yearly_aggregations import YearlyAggregation
from data_models import engine


logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)


def aggregate_by_year():
    with Session(engine) as session:
        results = session.query(
            WeatherData.station_id,
            func.extract('year', WeatherData.date).label('year'),
            (func.avg(WeatherData.max_temp) / 10).label('avg_max_temp'),
            (func.avg(WeatherData.min_temp) / 10).label('avg_min_temp'),
            (func.sum(WeatherData.precipitation) / 100).label('total_precipitation')
        ).group_by(
            WeatherData.station_id,
            func.extract('year', WeatherData.date),
        ).all()

        for result in results:
            logger.info(f'Adding analysis for {result.station_id} for year {result.year}')

            summary = YearlyAggregation(
                station_id=result.station_id, 
                year=result.year,
                avg_max_temp=result.avg_max_temp,
                avg_min_temp=result.avg_min_temp,
                total_precipitation=result.total_precipitation
            )
            session.add(summary)

        session.commit()
