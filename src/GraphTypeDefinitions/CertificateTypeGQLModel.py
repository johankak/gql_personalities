import asyncio
import dataclasses
import datetime
import typing
import strawberry

import strawberry.types
from uoishelpers.gqlpermissions import (
    OnlyForAuthentized,
    SimpleInsertPermission, 
    SimpleUpdatePermission, 
    SimpleDeletePermission
)    
from uoishelpers.resolvers import (
    getLoadersFromInfo, 
    createInputs,
    createInputs2,

    InsertError, 
    Insert, 
    UpdateError, 
    Update, 
    DeleteError, 
    Delete,

    PageResolver,
    VectorResolver,
    ScalarResolver
)
from uoishelpers.gqlpermissions.LoadDataExtension import LoadDataExtension
from uoishelpers.gqlpermissions.RbacProviderExtension import RbacProviderExtension
from uoishelpers.gqlpermissions.UserRoleProviderExtension import UserRoleProviderExtension
from uoishelpers.gqlpermissions.UserAbsoluteAccessControlExtension import UserAbsoluteAccessControlExtension

from .BaseGQLModel import BaseGQLModel, IDType, Relation

# Dopředná deklarace pro rekurzivní typy
CertificateTypeGQLModel = typing.Annotated["CertificateTypeGQLModel", strawberry.lazy(".CertificateTypeGQLModel")]

@createInputs2
class CertificateTypeInputFilter:
    name: str
    path: str
    id: IDType
    master_certificate_type_id: IDType 

@strawberry.federation.type(
    description="""Entity representing a CertificateType in a tree structure""",
    keys=["id"]
)
class CertificateTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).CertificateTypeModel

    path: typing.Optional[str] = strawberry.field(
        description="""Materialized path representing the hierarchy location.""",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""CertificateType name""",
        permission_classes=[OnlyForAuthentized]
    )

    master_certificate_type_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="""Parent type ID (master_certificate_type_id)""",
        permission_classes=[OnlyForAuthentized]
    )

    master_certificate_type: typing.Optional["CertificateTypeGQLModel"] = strawberry.field(
        description="""Parent certificate type""",
        permission_classes=[OnlyForAuthentized],
        resolver=ScalarResolver["CertificateTypeGQLModel"](fkey_field_name="master_certificate_type_id")
    )

    sub_certificate_types: typing.List["CertificateTypeGQLModel"] = strawberry.field(
        description="""Child certificate types (sub-types)""",
        permission_classes=[OnlyForAuthentized],
        resolver=VectorResolver["CertificateTypeGQLModel"](fkey_field_name="master_certificate_type_id", whereType=CertificateTypeInputFilter)
    )

@strawberry.interface(
    description="""CertificateType queries"""
)
class CertificateTypeQuery:
    certificate_type_by_id: typing.Optional[CertificateTypeGQLModel] = strawberry.field(
        description="""Get a CertificateType by its id""",
        permission_classes=[OnlyForAuthentized],
        resolver=CertificateTypeGQLModel.load_with_loader
    )

    certificate_type_page: typing.List[CertificateTypeGQLModel] = strawberry.field(
        description="""Get a page of CertificateTypes""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[CertificateTypeGQLModel](whereType=CertificateTypeInputFilter)
    )

from uoishelpers.resolvers import TreeInputStructureMixin, InputModelMixin

@strawberry.input(
    description="""Input type for creating a CertificateType"""
)
class CertificateTypeInsertGQLModel(TreeInputStructureMixin):
    getLoader = CertificateTypeGQLModel.getLoader
    
    master_certificate_type_id: typing.Optional[IDType] = strawberry.field(
        description="""Parent CertificateType id""",
        default=None
    )
    
    name: typing.Optional[str] = strawberry.field(
        description="""CertificateType name""",
        default=None
    )
    
    id: typing.Optional[IDType] = strawberry.field(
        description="""CertificateType id""",
        default=None
    )
    
    # Rekurzivní vkládání dětí
    sub_certificate_types: typing.Optional[typing.List["CertificateTypeInsertGQLModel"]] = strawberry.field(
        description="Child CertificateTypes",
        default_factory=list
    )

    createdby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="""Input type for updating a CertificateType"""
)
class CertificateTypeUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""CertificateType id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="Timestamp of last change"
    )
    name: typing.Optional[str] = strawberry.field(
        description="""CertificateType name""",
        default=None
    )
    
    master_certificate_type_id: typing.Optional[IDType] = strawberry.field(
        description="""Parent CertificateType id""",
        default=None
    )
    
    changedby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="""Input type for deleting a CertificateType"""
)
class CertificateTypeDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""CertificateType id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""Last change timestamp""",
    )


@strawberry.interface(
    description="""CertificateType mutations"""
)
class CertificateTypeMutation:
    @strawberry.mutation(
        description="""Insert a CertificateType (supports tree structure)""",
        permission_classes=[OnlyForAuthentized],
        extensions=[
            UserAbsoluteAccessControlExtension(roles=["administrátor"])
        ]
    )
    async def certificate_type_insert(
        self,
        info: strawberry.Info,
        certificate_type: CertificateTypeInsertGQLModel,
        user_roles: typing.List[typing.Any] = None
    ) -> typing.Union[CertificateTypeGQLModel, InsertError[CertificateTypeGQLModel]]:
        return await Insert[CertificateTypeGQLModel].DoItSafeWay(info=info, entity=certificate_type)
    

    @strawberry.mutation(
        description="""Update a CertificateType""",
        permission_classes=[OnlyForAuthentized],
        extensions=[
            UserAbsoluteAccessControlExtension(roles=["administrátor"])
        ]
    )
    async def certificate_type_update(
        self,
        info: strawberry.Info,
        certificate_type: CertificateTypeUpdateGQLModel,
        user_roles: typing.List[typing.Any] = None
    ) -> typing.Union[CertificateTypeGQLModel, UpdateError[CertificateTypeGQLModel]]:
        return await Update[CertificateTypeGQLModel].DoItSafeWay(info=info, entity=certificate_type)
    

    @strawberry.mutation(
        description="""Delete a CertificateType""",
        permission_classes=[OnlyForAuthentized],
        extensions=[
            UserAbsoluteAccessControlExtension(roles=["administrátor"])
        ]
    )   
    async def certificate_type_delete(
        self,
        info: strawberry.Info,
        certificate_type: CertificateTypeDeleteGQLModel,
        user_roles: typing.List[typing.Any] = None
    ) -> typing.Optional[DeleteError[CertificateTypeGQLModel]]:
        return await Delete[CertificateTypeGQLModel].DoItSafeWay(info=info, entity=certificate_type)