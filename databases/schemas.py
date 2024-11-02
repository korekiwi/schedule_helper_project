from pydantic import BaseModel
from datetime import date


class HomeworkPostDTO(BaseModel):
    user_id: int
    subject: str
    text: str
    date: date
    finished: bool


class HomeworkGetDTO(HomeworkPostDTO):
    id: int
