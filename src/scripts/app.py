from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate

from data_models import engine
from data_models.weather_data import WeatherData
from data_models.yearly_aggregations import YearlyAggregation


app = FastAPI()
add_pagination(app)

@app.get("/")
async def root():
    # with Session(engine) as session:
    return {"message": "Hello World"}


class WeatherDataPydantic(BaseModel):
    station_id: str
    date: date
    max_temp: Optional[float]
    min_temp: Optional[float]
    precipitation: Optional[float]

class YearlyAggregationsPydantic(BaseModel):
    station_id: str
    year: int
    avg_max_temp: Optional[float]
    avg_min_temp: Optional[float]
    total_precipitation: Optional[float]


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


@app.get("/api/weather/", response_model=Page[WeatherDataPydantic])
async def get_weather_record(station_id: str = 'USC00110072', date: str = None, session: Session = Depends(get_db)):
    if date:
        date = datetime.strptime(date, '%Y-%m-%d').date()
        return paginate(session, select(WeatherData).filter_by(station_id=station_id, date=date))
    else:
        return paginate(session, select(WeatherData).filter_by(station_id=station_id))


@app.get("/api/weather/stats/", response_model=Page[YearlyAggregationsPydantic])
async def get_weather_stats_record(station_id: str = 'USC00110072', year: int = None, session: Session = Depends(get_db)):
    if year:
        return paginate(session, select(YearlyAggregation).filter_by(station_id=station_id, year=year))
    else:
        return paginate(session, select(YearlyAggregation).filter_by(station_id=station_id))
