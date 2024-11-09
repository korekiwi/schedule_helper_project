from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (MetaData, Column, Integer,
                        String, Text, Time, Enum, Date, Boolean, ForeignKey)
from enum import Enum as En


metadata = MetaData()


class Base(DeclarativeBase):
    pass


class DayOfWeek(En):
    Monday = 'Понедельник'
    Tuesday = 'Вторник'
    Wednesday = 'Среда'
    Thursday = 'Четверг'
    Friday = 'Пятница'
    Saturday = 'Суббота'
    Sunday = 'Воскресенье'


class Homework(Base):
    __tablename__ = 'homework'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    subject = Column(String(100))
    text = Column(Text(1000))
    date = Column(Date)
    finished = Column(Boolean, default=False)


class Schedule(Base):
    __tablename__ = 'schedule'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    day = Column(Enum(DayOfWeek))
    time_start = Column(Time)
    time_end = Column(Time)
    text = Column(Text(255))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer)
    hw_notifications = Column(Boolean)
    schedule_notifications = Column(Boolean)
