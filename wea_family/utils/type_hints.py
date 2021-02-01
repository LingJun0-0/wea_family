from datetime import datetime, date
from typing import Type, Union, List, Dict

from pandas import Timestamp, Series
from bson import ObjectId

DatetimeLike = Union[str, datetime, date, Timestamp]

Number = Union[float, int]

ObjectIdLike = Union[str, ObjectId]

SingleOrMany = Union[ObjectIdLike, List[str], List[ObjectId]]
