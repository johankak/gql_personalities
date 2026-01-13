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

class UserCertificateTypeModel(BaseModel):
    """
    Model pro evidenci certifikátů získaných uživatelem.
    """
    __tablename__ = "user_certificatetypes"
    
    # Datum získání/platnosti certifikátu
    startdate: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True)
    
    # Datum expirace certifikátu
    enddate: Mapped[datetime.datetime] = mapped_column(default=None, nullable=True)
    
    # ID uživatele
    user_id: Mapped[IDType] = UUIDFKey(nullable=True)
    
    # ID typu certifikátu (katalog CertificateTypeModel)
    certificate_type_id: Mapped[IDType] = mapped_column(ForeignKey("certificatetypes.id"), default=None, nullable=True)