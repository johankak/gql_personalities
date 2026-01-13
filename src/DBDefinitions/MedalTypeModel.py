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

class MedalTypeModel(BaseModel):
    """
    Katalog typů medailí.
    """
    __tablename__ = "medaltypes"

    # --- Konfigurace stromu ---
    path_attribute_name = "path"
    parent_attribute_name = "master_medaltype"
    parent_id_attribute_name = "master_medaltype_id"
    children_attribute_name = "sub_medaltypes"

    # Materialized path
    path: Mapped[str] = mapped_column(
        index=True,
        nullable=True,
        default=None,
        comment="Materialized path technique"
    )

    # Název medaile/ocenění
    name: Mapped[str] = mapped_column(default=None, nullable=True)

    # ID nadřízené kategorie medailí
    master_medaltype_id: Mapped[IDType] = mapped_column(
        ForeignKey("medaltypes.id"),
        nullable=True,
        default=None,
        index=True,
    )

    # Relace na rodiče
    master_medaltype = relationship(
        "MedalTypeModel",
        viewonly=True, 
        remote_side="MedalTypeModel.id",
        uselist=False,
        back_populates="sub_medaltypes",
    )

    # Relace na podřízené typy medailí
    sub_medaltypes = relationship(
        "MedalTypeModel",
        back_populates="master_medaltype",
        uselist=True,
        init=True,
        cascade="save-update"
    )