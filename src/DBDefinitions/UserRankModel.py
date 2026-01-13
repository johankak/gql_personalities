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

class UserRankModel(BaseModel):
    """
    Model pro přiřazení hodnosti (Rank) uživateli.
    Sleduje historii hodností díky časovému omezení (startdate/enddate).
    """
    __tablename__ = "user_ranks"
    
    # Datum získání hodnosti
    startdate: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True)
    
    # Datum ukončení platnosti hodnosti (např. při povýšení)
    enddate: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True)
    
    # ID uživatele
    user_id: Mapped[IDType] = UUIDFKey(nullable=True)
    
    # ID hodnosti z katalogu (RankModel)
    rank_id: Mapped[IDType] = mapped_column(ForeignKey("ranks.id"), default=None, nullable=True)