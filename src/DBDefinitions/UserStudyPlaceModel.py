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

class UserStudyPlaceModel(BaseModel):
    """
    Eviduje vazbu mezi uživatelem a studijním místem (např. studium na škole).
    """
    __tablename__ = "user_studyplaces"
    
    # Datum nástupu ke studiu
    startdate: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True)
    
    # Datum ukončení studia
    enddate: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True)
    
    # ID studenta/uživatele
    user_id: Mapped[IDType] = UUIDFKey(nullable=True)
    
    # ID školy (StudyPlaceModel)
    studyplace_id: Mapped[IDType] = mapped_column(ForeignKey("studyplaces.id"), default=None, nullable=True)