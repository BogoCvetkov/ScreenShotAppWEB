from sqlalchemy import select, cast, String, VARCHAR


class BaseMixin:

    def create(self,session):
        session.add(self)
        session.commit()

    @classmethod
    def get_by_id(cls,session,id):
        result = session.get(cls,id)
        return result

    @classmethod
    def search(cls,session,**kwargs):
        stmt = select(cls)
        for col in kwargs.keys():
            if col in cls.__table__.columns.keys():
                if isinstance(cls.__dict__[col].type, String):
                    stmt = stmt.where(cls.__dict__[col].ilike(f"{kwargs[col]}%"))

        result = session.execute(stmt).all()
        result = [res[0] for res in result]
        return result

    @classmethod
    def get_all(cls,session):
        result = session.execute(select(cls)).all()
        result = [res[0] for res in result]
        return result

    def delete(self,session):
        session.delete(self)
        session.commit()