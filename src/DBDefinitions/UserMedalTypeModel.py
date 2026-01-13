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

class UserMedalTypeModel(BaseModel):
    """
    Model reprezentující přiřazení konkrétního typu medaile konkrétnímu uživateli.
    """
    __tablename__ = "user_medaltypes"
    
    startdate: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True)
    
    enddate: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True)
    
    # Cizí klíč na uživatele
    user_id: Mapped[IDType] = UUIDFKey(nullable=True)
    
    # Cizí klíč na typ medaile (katalog MedalTypeModel)
    medaltype_id: Mapped[IDType] = mapped_column(ForeignKey("medaltypes.id"), default=None, nullable=True)