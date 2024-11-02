from sqlalchemy import create_engine, select, delete, update, func, and_
from sqlalchemy.orm import Session
from datetime import time

from databases.database_settings import get_mysql_url
from databases.models import metadata, Base, Homework, Schedule, DayOfWeek
from databases.schemas import HomeworkPostDTO, HomeworkGetDTO

engine = create_engine(
    url=get_mysql_url(),
    # echo=True
)

Base.metadata.create_all(bind=engine)


def create_homework(user_id, subject, text, date):
    with Session(autoflush=False, bind=engine) as db:
        new_homework = Homework(user_id=user_id,
                                subject=subject,
                                text=text,
                                date=date)
        db.add(new_homework)
        db.commit()


def get_all_subjects(user_id):
    with Session(autoflush=False, bind=engine) as db:
        q = (
            select(Homework.subject)
            .filter(Homework.user_id == user_id)
        )
        subjects = db.execute(q).scalars().unique().all()
        return(subjects)


def get_homework_by_subject(user_id, subject):
    with Session(autoflush=False, bind=engine) as db:
        q = (
            select(Homework)
            .filter(and_(Homework.user_id == user_id, Homework.subject == subject))
        )
        all_homework = db.execute(q).scalars().all()
        res = [HomeworkGetDTO.model_validate(homework, from_attributes=True) for homework in all_homework]
        return(res)


def delete_all_finished_tasks(user_id):
    with Session(autoflush=False, bind=engine) as db:
        q = (
            delete(Homework)
            .filter(and_(Homework.user_id == user_id, Homework.finished == 1))
        )
        db.execute(q)
        db.commit()


def delete_all_finished_tasks_by_subject(user_id, subject):
    with Session(autoflush=False, bind=engine) as db:
        q = (
            delete(Homework)
            .filter(and_(Homework.user_id == user_id, Homework.finished == 1, Homework.subject == subject))
        )
        db.execute(q)
        db.commit()


def check_task_id(user_id, task_id):
    with Session(autoflush=False, bind=engine) as db:
        q = (
            select(Homework.user_id)
            .filter(Homework.id == task_id)
        )
        got_user_id = db.execute(q).scalars().first()
        return True if got_user_id == user_id else False


def delete_task_by_id(user_id, task_id):
    with Session(autoflush=False, bind=engine) as db:
        q = (
            delete(Homework)
            .filter(and_(Homework.id == task_id, Homework.user_id == user_id))
        )
        db.execute(q)
        db.commit()


def hard_delete(user_id):
    with Session(autoflush=False, bind=engine) as db:
        q = (
            delete(Homework)
            .filter(Homework.user_id == user_id)
        )
        db.execute(q)
        db.commit()


def change_status(user_id, task_id, new_status):
    with Session(autoflush=False, bind=engine) as db:
        q = (
            update(Homework)
            .filter(and_(Homework.user_id == user_id, Homework.id == task_id))
            .values(finished=new_status)
        )
        db.execute(q)
        db.commit()


if __name__ == '__main__':
    #print(get_all_subjects(1167336636))
    # delete_all_finished_tasks(1167336636)
    # print(check_task_id(1167336636, 12))
    change_status(533078883, 5, 1)
