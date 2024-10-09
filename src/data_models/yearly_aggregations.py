from typing import Optional


from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Float, String
from data_models import Base


class YearlyAggregation(Base):
    __tablename__ = "yearly_aggregations"

    station_id:            Mapped[str]            =  mapped_column(String(12), primary_key=True)
    year:                  Mapped[int]            =  mapped_column(Integer, primary_key=True)

    avg_max_temp:          Mapped[Optional[float]]  =  mapped_column(Float)      # degrees Celsius
    avg_min_temp:          Mapped[Optional[float]]  =  mapped_column(Float)      # degrees Celsius
    total_precipitation:   Mapped[Optional[float]]  =  mapped_column(Float)      # centimeter

    def __repr__(self) -> str:
        return f"""YearlyAggregation(
            station_id={self.station_id}, 
            year={self.year},
            avg_max_temp={"Nan" if self.avg_max_temp is None else self.avg_max_temp} C, 
            avg_min_temp={"Nan" if self.avg_min_temp is None else self.avg_min_temp} C, 
            total_precipitation={"NaN" if self.total_precipitation is None else self.total_precipitation} cm
        )"""
