from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData, Table, Column, Integer, String, Text, Time, Enum, Date, Boolean
from enum import Enum as En


metadata = MetaData()

class Base(DeclarativeBase):
    pass


class DayOfWeek(En):
    Monday = 'Monday'
    Tuesday = 'Tuesday'
    Wednesday = 'Wednesday'
    Thursday = 'Thursday'
    Friday = 'Friday'
    Saturday = 'Saturday'
    Sunday = 'Sunday'


class Homework(Base):
    __tablename__ = 'homework'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    subject = Column(String(100))
    text = Column(Text(1000))
    date = Column(Date)
    finished = Column(Boolean, default=False)


class Schedule(Base):
    __tablename__ = 'schedule'

    id = Column(Integer, primary_key=True)
    day = Column(Enum(DayOfWeek))
    time_start = Column(Time)
    time_end = Column(Time)
    text = Column(Text(255))
    finished = Column(Boolean)

