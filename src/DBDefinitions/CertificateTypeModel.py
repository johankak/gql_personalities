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

class CertificateTypeModel(BaseModel):
    """
    Katalog typů certifikátů.
    """
    __tablename__ = "certificatetypes"

    # --- Konfigurace stromu ---
    path_attribute_name = "path"
    parent_attribute_name = "master_certificate_type"
    parent_id_attribute_name = "master_certificate_type_id"
    children_attribute_name = "sub_certificate_types"

    # Materialized path pro strom
    path: Mapped[str] = mapped_column(
        index=True,
        nullable=True,
        default=None,
        comment="Materialized path technique"
    )

    # Název certifikátu
    name: Mapped[str] = mapped_column(default=None, nullable=True)

    # ID nadřízeného typu certifikátu
    master_certificate_type_id: Mapped[IDType] = mapped_column(
        ForeignKey("certificatetypes.id"),
        nullable=True,
        default=None,
        index=True,
    )

    # Relace na rodiče
    master_certificate_type = relationship(
        "CertificateTypeModel",
        viewonly=True, 
        remote_side="CertificateTypeModel.id",
        uselist=False,
        back_populates="sub_certificate_types",
    )

    # Relace na podřízené typy (děti)
    sub_certificate_types = relationship(
        "CertificateTypeModel",
        back_populates="master_certificate_type",
        uselist=True,
        init=True,
        cascade="save-update"
    )