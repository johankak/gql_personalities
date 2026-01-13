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

class RankModel(BaseModel):
    """
    Katalog hodností
    """
    __tablename__ = "ranks"

    # Název hodnosti
    name: Mapped[str] = mapped_column(default=None, nullable=True)