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

class StudyPlaceModel(BaseModel):
    __tablename__ = "studyplaces"

    # Konfigurace pro stromovou strukturu
    path_attribute_name = "path"
    parent_attribute_name = "master_studyplace"
    parent_id_attribute_name = "master_studyplace_id"
    children_attribute_name = "sub_studyplaces"
    
    # Materialized path column
    path: Mapped[str] = mapped_column(
        index=True,
        nullable=True,
        default=None,
        comment="Materialized path technique"
    )
    
    name: Mapped[str] = mapped_column(default=None, nullable=True)

    # Cizí klíč na rodiče
    master_studyplace_id: Mapped[IDType] = mapped_column(
        ForeignKey("studyplaces.id"),
        nullable=True,
        default=None,
        index=True,
    )

    # Relace na rodiče
    master_studyplace = relationship(
        "StudyPlaceModel",
        viewonly=True, 
        remote_side="StudyPlaceModel.id",
        uselist=False,
        back_populates="sub_studyplaces",
    )

    # Relace na děti
    sub_studyplaces = relationship(
        "StudyPlaceModel",
        back_populates="master_studyplace",
        uselist=True,
        init=True,
        cascade="save-update"
    )