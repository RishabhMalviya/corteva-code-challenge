from typing import Optional
from datetime import datetime


from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Date

from data_models import Base


class WeatherData(Base):
    __tablename__ = "weather_data"

    station_id:    Mapped[str]            =  mapped_column(String(12), primary_key=True)
    date:          Mapped[datetime]       =  mapped_column(Date, primary_key=True)

    max_temp:      Mapped[Optional[int]]  =  mapped_column(Integer)      # tenths of degree Celsius
    min_temp:      Mapped[Optional[int]]  =  mapped_column(Integer)      # tenths of degree Celsius
    precipitation: Mapped[Optional[int]]  =  mapped_column(Integer)      # tenths of millimeter

    def __repr__(self) -> str:
        return f"""WeatherData(
            station_id={self.station_id}, 
            date={self.date}, 
            max_temp={"Nan" if self.max_temp is None else self.max_temp/10} C, 
            min_temp={"Nan" if self.min_temp is None else self.min_temp/10} C, 
            precipitation={"NaN" if self.precipitation is None else self.precipitation/10} mm
        )"""
