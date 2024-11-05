from pydantic import BaseModel
from datetime import date, time

from databases.models import DayOfWeek


class HomeworkPostDTO(BaseModel):
    user_id: int
    subject: str
    text: str
    date: date
    finished: bool


class HomeworkGetDTO(HomeworkPostDTO):
    id: int


class SchedulePostDTO(BaseModel):
    user_id: int
    day: DayOfWeek
    time_start: time
    time_end: time
    text: str


class ScheduleGetDTO(SchedulePostDTO):
    id: int
