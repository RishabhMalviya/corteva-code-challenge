import os

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

import numpy as np
import pandas as pd
from sqlalchemy.orm import Session

from data_models.weather_data import WeatherData
from data_models import engine


logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger)


def _convert_row_to_orm_model(row) -> WeatherData:
    return WeatherData(
        station_id=row.station_id,
        date=row.date,
        max_temp=row.max_temp,
        min_temp=row.min_temp,
        precipitation=row.precipitation
    )


def _read_wx_data_file(filepath: str) -> pd.DataFrame:
    station_id = filepath.split('/')[-1].split('.')[0]

    df = pd.read_fwf(
        filepath,
        widths=[8,6,6,6],
        names=['date', 'max_temp', 'min_temp', 'precipitation']
    )

    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    df[['max_temp', 'min_temp', 'precipitation']] = df[['max_temp', 'min_temp', 'precipitation']].replace(-9999, np.nan)
    df['station_id'] = station_id

    return station_id, df


def ingest_file(filepath: str):
    station_id, df = _read_wx_data_file(filepath)

    with Session(engine) as session:
        session.add_all([
            _convert_row_to_orm_model(row) for _, row in df.iterrows()
        ])

        session.commit()

        result = session.query(WeatherData).filter_by(station_id=station_id).all()
        logger.debug(f'{len(result)} records inserted for dates from {result[0].date} to {result[-1].date} for station ID {station_id}')


def ingest_data(num_files: int = -1):
    directory = 'data/wx_data'
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    files = files[:min(num_files,len(files))] if not num_files == -1 else files
    
    for filepath in files:
        ingest_file(filepath)
