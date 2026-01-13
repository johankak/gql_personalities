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

class UserWorkHistoryPositionModel(BaseModel):
    """
    Eviduje pracovní historii uživatele (přiřazení k pracovním pozicím v čase).
    """
    __tablename__ = "user_workhistorypositions"
    
    # Datum nástupu na pozici
    startdate: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True)
    
    # Datum odchodu z pozice
    enddate: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True)
    
    # ID uživatele
    user_id: Mapped[IDType] = UUIDFKey(nullable=True)
    
    # ID pracovní pozice (WorkHistoryPositionModel)
    workhistoryposition_id: Mapped[IDType] = mapped_column(ForeignKey("workhistorypositions.id"), default=None, nullable=True)