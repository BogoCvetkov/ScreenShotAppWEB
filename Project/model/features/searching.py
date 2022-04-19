from sqlalchemy import select, update, cast, String, VARCHAR, Integer, DateTime, Boolean
from datetime import datetime
import operator

operatorMap = { ">": operator.gt, "<": operator.lt, "=": operator.eq }


# Function for searching and filtering based on the available fields for a model
def filter_sort(model, queries):
    stmt = select(model)
    for col in queries.keys():
        if col in model.__table__.columns.keys():
            if isinstance(model.__dict__[col].type, String):
                stmt = stmt.where(
                    model.__dict__[col].ilike(f"%{queries[col]}%"))
            if isinstance(model.__dict__[col].type, Integer):
                # expression example - ">,5", "=,5" etc..
                exp = queries[col].split(",")
                if operatorMap.get(exp[0], None):
                    stmt = stmt.where(
                        operatorMap[exp[0]](
                            model.__dict__[col], int(exp[1])))
            if isinstance(model.__dict__[col].type, DateTime):
                # expression example - ">,date", "<,date"
                exp = queries[col].split(",")
                date = datetime.fromtimestamp(round(int(exp[1])))
                if operatorMap.get(exp[0], None):
                    stmt = stmt.where(
                        operatorMap[exp[0]](
                            model.__dict__[col], date))
            if isinstance(model.__dict__[col].type, Boolean):
                if queries[col].lower() == "false":
                    stmt = stmt.where(
                        model.__dict__[col].is_(False))
                else:
                    stmt = stmt.where(
                        model.__dict__[col].is_(True))

    if queries.get("sort", None):
        # expression example - "desc,Column-name", "asc,Column-name"
        exp = queries["sort"].split(",")
        try:
            if exp[1] in model.__table__.columns.keys():
                if exp[0] == "desc":
                    stmt = stmt.order_by(model.__dict__[exp[1]].desc())
                if exp[0] == "asc":
                    stmt = stmt.order_by(model.__dict__[exp[1]].asc())
        except:
            pass

    return stmt