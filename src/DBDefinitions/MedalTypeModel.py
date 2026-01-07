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
class MedalTypeModel(BaseModel):
    __tablename__ = "medaltypes"

    # Konfigurace pro stromovou strukturu (shodne se StudyPlace)
    path_attribute_name = "path"
    parent_attribute_name = "master_medaltype"
    parent_id_attribute_name = "master_medaltype_id"
    children_attribute_name = "sub_medaltypes"

    # Materialized path column
    path: Mapped[str] = mapped_column(
        index=True,
        nullable=True,
        default=None,
        comment="Materialized path technique"
    )

    name: Mapped[str] = mapped_column(default=None, nullable=True)

    # Cizí klíč na rodiče (odpovida klici v JSONu: master_medaltype_id)
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

    # Relace na děti
    sub_medaltypes = relationship(
        "MedalTypeModel",
        back_populates="master_medaltype",
        uselist=True,
        init=True,
        cascade="save-update"
    )