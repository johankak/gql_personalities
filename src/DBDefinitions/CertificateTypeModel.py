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

###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#
###########################################################################################################################
class CertificateTypeModel(BaseModel):
    __tablename__ = "personalitiescertificatetypes"

    # Materialized path technique
    
    parent_attribute_name = "parent"
    path_attribute_name = "path"
    children_attribute_name = "children"
    parent_id_attribute_name = "parent_id"
    
    name: Mapped[str] = mapped_column(default=None, nullable=True)

    