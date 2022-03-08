from sqlalchemy import Column, String, Integer, Boolean
from Project.app.model.common.base_mixin import BaseMixin
from Project.app.model import Base


class UserModel(Base, BaseMixin):

    __tablename__ = "users"

    id = Column(Integer,primary_key=True)
    email = Column(String,unique=True,nullable=False)
    username = Column(String,unique=True,nullable=False)
    password = Column(String,nullable=False)
    admin = Column(Boolean,default=False)