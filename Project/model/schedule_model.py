from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy import select
from Project.model.common.base_mixin import BaseMixin
from Project.model.DB import Base


class ScheduleModel(Base, BaseMixin):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True)
    day = Column(Integer)
    hour = Column(Integer)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"),
                        nullable=False)

    @classmethod
    def search_schedules(cls, session, hour=None, weekday=None):
        stmt = select(cls)

        if hour != None:
            stmt = stmt.where(cls.hour == hour)

        if weekday != None:
            stmt = stmt.where(cls.day == weekday)

        result = session.scalars(stmt).all()

        return result