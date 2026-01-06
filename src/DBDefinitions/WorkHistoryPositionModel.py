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
from sqlalchemy.orm import Mapped, mapped_column, synonym, relationship

from .BaseModel import BaseModel, UUIDColumn, UUIDFKey, IDType

###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#
###########################################################################################################################
class WorkHistoryPositionModel(BaseModel):
    __tablename__ = "workhistorypositions"

    # Konfigurace pro stromovou strukturu (názvy atributů v tomto modelu)
    path_attribute_name = "path"
    parent_attribute_name = "master_workhistoryposition"
    parent_id_attribute_name = "master_workhistoryposition_id"
    children_attribute_name = "sub_workhistorypositions"
    
    # Materialized path column
    path: Mapped[str] = mapped_column(
        index=True,
        nullable=True,
        default=None,
        comment="Materialized path technique"
    )
    
    name: Mapped[str] = mapped_column(default=None, nullable=True)

    # Cizí klíč na rodiče
    master_workhistoryposition_id: Mapped[IDType] = mapped_column(
        ForeignKey("workhistorypositions.id"),
        nullable=True,
        default=None,
        index=True,
    )

    # Relace na rodiče
    master_workhistoryposition = relationship(
        "WorkHistoryPositionModel",
        viewonly=True, 
        remote_side="WorkHistoryPositionModel.id",
        uselist=False,
        back_populates="sub_workhistorypositions",
    )

    # Relace na děti
    sub_workhistorypositions = relationship(
        "WorkHistoryPositionModel",
        back_populates="master_workhistoryposition",
        uselist=True,
        init=True,
        cascade="save-update"
    )