from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.orm import relationship
from Project.model.common.base_mixin import BaseMixin
from Project.model.DB import Base


class AccountModel(Base, BaseMixin):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    email_body = Column(String, default=" ")
    active = Column(Boolean, default=True)
    last_scrape_fail = Column(Boolean, default=False)
    last_email_fail = Column(Boolean, default=False)
    last_scraped = Column(DateTime)
    last_emailed = Column(DateTime)
    country = Column(String, default="ALL")
    pages = relationship("PageModel",
                         cascade="all,delete-orphan",
                         backref="account",
                         passive_deletes=True)
    keywords = relationship("KeywordModel",
                            cascade="all,delete-orphan",
                            backref="account",
                            passive_deletes=True)
    screenshot = relationship("ScreenShotModel", uselist=False, backref="account",
                              cascade="all,delete-orphan", passive_deletes=True)
    logs = relationship("LogModel", backref="account",
                        cascade="all,delete-orphan", passive_deletes=True)
    schedules = relationship("ScheduleModel", backref="account",
                             cascade="all,delete-orphan", passive_deletes=True)