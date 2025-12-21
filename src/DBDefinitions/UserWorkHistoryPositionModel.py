import typing
import datetime
import dataclasses
import sqlalchemy
from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, synonym

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, column_property

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#
###########################################################################################################################
class UserWorkHistoryPositionModel(BaseModel):
    __tablename__ = "user_workhistorypositions"

    path_attribute_name = "path"
    parent_attribute_name = "masterevent"
    parent_id_attribute_name = "masterevent_id"
    children_attribute_name = "subevents"

    # Materialized path technique
    
    startdate: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True)
    enddate: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True)
    user_id: Mapped[IDType] = UUIDFKey(nullable=True)
    workhistoryposition_id: Mapped[IDType] = mapped_column(ForeignKey("workhistorypositions.id"), default=None, nullable=True)
