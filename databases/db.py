import datetime

from sqlalchemy import create_engine, select, delete, update, and_
from sqlalchemy.orm import Session

from databases.database_settings import get_mysql_url
from databases.models import Base, User, Homework, Schedule, DayOfWeek
from databases.schemas import (HomeworkGetDTO, ScheduleGetDTO)

engine = create_engine(
    url=get_mysql_url()
)

Base.metadata.create_all(bind=engine)


"""Homework"""


def create_user(tg_id):
    with Session(autoflush=False, bind=engine) as db:
        new_user = User(tg_id=tg_id,
                        hw_notifications=False,
                        schedule_notifications=False)
        db.add(new_user)
        db.commit()


def create_homework(tg_id, subject, text, date):
    with Session(autoflush=False, bind=engine) as db:
        user_id = get_user_id_by_tg_id(tg_id)
        if user_id is None:
            create_user(tg_id)
            db.commit()
            user_id = get_user_id_by_tg_id(tg_id)
        new_homework = Homework(user_id=user_id,
                                subject=subject,
                                text=text,
                                date=date)
        db.add(new_homework)
        db.commit()


def get_all_subjects(tg_id):
    with Session(autoflush=False, bind=engine) as db:
        q = (
            select(Homework.subject)
            .join(User, Homework.user_id == User.id)
            .filter(User.tg_id == tg_id)
        )
        subjects = db.execute(q).scalars().unique().all()
        return subjects


def get_homework_by_subject(tg_id, subject):
    with Session(autoflush=False, bind=engine) as db:
        q = (
            select(Homework)
            .join(User, Homework.user_id == User.id)
            .filter(and_(User.tg_id == tg_id, Homework.subject == subject))
        )
        all_homework = db.execute(q).scalars().all()
        res = [HomeworkGetDTO.model_validate(homework, from_attributes=True) for homework in all_homework]
        return res


def get_all_unfinished_homework():
    with Session(autoflush=False, bind=engine) as db:
        q = (
            select(Homework)
            .filter(Homework.finished == 0)
        )
        all_homework = db.execute(q).scalars().all()
        res = [HomeworkGetDTO.model_validate(homework, from_attributes=True) for homework in all_homework]
        return res


def delete_all_finished_tasks(tg_id):
    with Session(autoflush=False, bind=engine) as db:
        user_id = get_user_id_by_tg_id(tg_id)
        q = (
            delete(Homework)
            .filter(and_(Homework.user_id == user_id, Homework.finished == 1))
        )
        db.execute(q)
        db.commit()


def delete_all_finished_tasks_by_subject(tg_id, subject):
    with Session(autoflush=False, bind=engine) as db:
        user_id = get_user_id_by_tg_id(tg_id)
        q = (
            delete(Homework)
            .filter(and_(Homework.user_id == user_id, Homework.finished == 1, Homework.subject == subject))
        )
        db.execute(q)
        db.commit()


def check_task_id(tg_id, task_id):
    with Session(autoflush=False, bind=engine) as db:
        q = (
            select(User.tg_id)
            .select_from(User)
            .join(Homework, Homework.user_id == User.id)
            .filter(Homework.id == task_id)
        )
        got_tg_id = db.execute(q).scalars().first()
        return True if got_tg_id == tg_id else False


def get_user_id_by_tg_id(tg_id):
    with Session(autoflush=False, bind=engine) as db:
        q = (
            select(User.id)
            .filter(User.tg_id == tg_id)
        )
        user_id = db.execute(q).scalars().first()
        return user_id


def get_tg_id_by_user_id(user_id):
    with Session(autoflush=False, bind=engine) as db:
        q = (
            select(User.tg_id)
            .filter(User.id == user_id)
        )
        tg_id = db.execute(q).scalars().first()
        return tg_id


def delete_task_by_id(tg_id, task_id):
    with Session(autoflush=False, bind=engine) as db:
        user_id = get_user_id_by_tg_id(tg_id)
        q = (
            delete(Homework)
            .filter(and_(Homework.id == task_id, Homework.user_id == user_id))
        )
        db.execute(q)
        db.commit()


def hard_delete(tg_id):
    with Session(autoflush=False, bind=engine) as db:
        user_id = get_user_id_by_tg_id(tg_id)
        q = (
            delete(Homework)
            .filter(Homework.user_id == user_id)
        )
        db.execute(q)
        db.commit()


def change_status(tg_id, task_id, new_status):
    with Session(autoflush=False, bind=engine) as db:
        user_id = get_user_id_by_tg_id(tg_id)
        q = (
            update(Homework)
            .filter(and_(Homework.user_id == user_id, Homework.id == task_id))
            .values(finished=new_status)
        )
        db.execute(q)
        db.commit()


"""Schedule"""


def create_schedule_task(tg_id, days, time_start, time_end, text):
    with Session(autoflush=False, bind=engine) as db:
        user_id = get_user_id_by_tg_id(tg_id)
        if user_id is None:
            create_user(tg_id)
            db.commit()
            user_id = get_user_id_by_tg_id(tg_id)
        new_tasks = []
        for day in days:
            new_task = Schedule(user_id=user_id,
                                day=day,
                                time_start=time_start,
                                time_end=time_end,
                                text=text)
            new_tasks.append(new_task)
    db.add_all(new_tasks)
    db.commit()


def get_schedule_tasks(tg_id, day):
    with Session(autoflush=False, bind=engine) as db:
        q = (
            select(Schedule)
            .join(User, Schedule.user_id == User.id)
            .filter(and_(Schedule.day == day, User.tg_id == tg_id))
            .order_by(Schedule.time_start)
        )
        all_tasks = db.execute(q).scalars().all()
        res = [ScheduleGetDTO.model_validate(task, from_attributes=True) for task in all_tasks]
        return res


def get_schedule_tasks_by_time_start_and_day(day, time_start):
    with Session(autoflush=False, bind=engine) as db:
        q = (
            select(Schedule)
            .filter(and_(Schedule.day == day, Schedule.time_start == time_start))
        )
        all_tasks = db.execute(q).scalars().all()
        res = [ScheduleGetDTO.model_validate(task, from_attributes=True) for task in all_tasks]
        return res


def delete_schedule_tasks_by_day(tg_id, day):
    with Session(autoflush=False, bind=engine) as db:
        user_id = get_user_id_by_tg_id(tg_id)
        q = (
            delete(Schedule)
            .filter(and_(Schedule.day == day, Schedule.user_id == user_id))
        )
        db.execute(q)
        db.commit()


def check_schedule_task_id(tg_id, task_id):
    with Session(autoflush=False, bind=engine) as db:
        q = (
            select(User.tg_id)
            .select_from(User)
            .join(Schedule, Schedule.user_id == User.id)
            .filter(Schedule.id == task_id)
        )
        got_tg_id = db.execute(q).scalars().first()
        return True if got_tg_id == tg_id else False


def delete_schedule_task_by_id(tg_id, task_id):
    with Session(autoflush=False, bind=engine) as db:
        user_id = get_user_id_by_tg_id(tg_id)
        q = (
            delete(Schedule)
            .filter(and_(Schedule.id == task_id, Schedule.user_id == user_id))
        )
        db.execute(q)
        db.commit()


def get_schedule_task_text_by_id(task_id):
    with Session(autoflush=False, bind=engine) as db:
        q = (
            select(Schedule.text)
            .filter(Schedule.id == task_id)
        )
        task_text = db.execute(q).scalars().first()
        return task_text


def delete_schedule_tasks_by_id(tg_id, task_id):
    with Session(autoflush=False, bind=engine) as db:
        task_text = get_schedule_task_text_by_id(task_id)
        user_id = get_user_id_by_tg_id(tg_id)
        q = (
            delete(Schedule)
            .filter(and_(Schedule.text == task_text, Schedule.user_id == user_id))
        )
        db.execute(q)
        db.commit()


def schedule_hard_delete(tg_id):
    with Session(autoflush=False, bind=engine) as db:
        user_id = get_user_id_by_tg_id(tg_id)
        q = (
            delete(Schedule)
            .filter(Schedule.user_id == user_id)
        )
        db.execute(q)
        db.commit()


"""Уведомления"""


def get_hw_notifications(tg_id):
    with Session(autoflush=False, bind=engine) as db:
        q = (
            select(User.hw_notifications)
            .filter(User.tg_id == tg_id)
        )
        res = db.execute(q).scalars().first()
        return res


def get_sched_notifications(tg_id):
    with Session(autoflush=False, bind=engine) as db:
        q = (
            select(User.schedule_notifications)
            .filter(User.tg_id == tg_id)
        )
        res = db.execute(q).scalars().first()
        return res


def change_hw_notifications(tg_id, change: int):
    with Session(autoflush=False, bind=engine) as db:
        q = (
            update(User)
            .where(User.tg_id == tg_id)
            .values(hw_notifications=change)
        )
        db.execute(q)
        db.commit()


def change_sched_notifications(tg_id, change: int):
    with Session(autoflush=False, bind=engine) as db:
        q = (
            update(User)
            .where(User.tg_id == tg_id)
            .values(schedule_notifications=change)
        )
        db.execute(q)
        db.commit()


