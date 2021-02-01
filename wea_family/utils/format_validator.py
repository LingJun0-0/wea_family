from datetime import date, datetime, time
from dateutil.parser import parse

from wea_family.utils.type_hints import ObjectId


def ensure_id(s) -> str:
    if isinstance(s, ObjectId):
        return str(s)
    return s


def ensure_datetime(dt) -> datetime:
    if isinstance(dt, datetime):
        return dt
    elif isinstance(dt, str):
        return parse(dt)
    elif isinstance(dt, date):
        return datetime.combine(dt, time.min)
    else:
        raise ValueError(f"bad type: {type(dt)}")

