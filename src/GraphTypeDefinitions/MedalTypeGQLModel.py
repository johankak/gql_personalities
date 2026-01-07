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
from uoishelpers.gqlpermissions.RbacInsertProviderExtension import RbacInsertProviderExtension
from uoishelpers.gqlpermissions.UserRoleProviderExtension import UserRoleProviderExtension
from uoishelpers.gqlpermissions.UserAccessControlExtension import UserAccessControlExtension
from uoishelpers.gqlpermissions.UserAbsoluteAccessControlExtension import UserAbsoluteAccessControlExtension

from .BaseGQLModel import BaseGQLModel, IDType, Relation

# Dopředná deklarace pro rekurzivní typy
MedalTypeGQLModel = typing.Annotated["MedalTypeGQLModel", strawberry.lazy(".MedalTypeGQLModel")]

@createInputs2
class MedalTypeInputFilter:
    name: str
    path: str
    level: int
    id: IDType
    master_medaltype_id: IDType

@strawberry.federation.type(
    description="""Entity representing a MedalType""",
    keys=["id"]
)
class MedalTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).MedalTypeModel

    path: typing.Optional[str] = strawberry.field(
        description="""Materialized path representing the hierarchy location.""",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""MedalType name""",
        permission_classes=[OnlyForAuthentized]
    )

    master_medaltype_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="""Parent MedalType ID""",
        permission_classes=[OnlyForAuthentized]
    )

    master_medaltype: typing.Optional["MedalTypeGQLModel"] = strawberry.field(
        description="""Parent MedalType""",
        permission_classes=[OnlyForAuthentized],
        resolver=ScalarResolver["MedalTypeGQLModel"](fkey_field_name="master_medaltype_id")
    )

    sub_medaltypes: typing.List["MedalTypeGQLModel"] = strawberry.field(
        description="""Child MedalTypes""",
        permission_classes=[OnlyForAuthentized],
        resolver=VectorResolver["MedalTypeGQLModel"](fkey_field_name="master_medaltype_id", whereType=MedalTypeInputFilter)
    )


@strawberry.interface(
    description="""MedalType queries"""
)
class MedalTypeQuery:
    MedalType_by_id: typing.Optional[MedalTypeGQLModel] = strawberry.field(
        description="""Get a MedalType by its id""",
        permission_classes=[OnlyForAuthentized],
        resolver=MedalTypeGQLModel.load_with_loader
    )

    MedalType_page: typing.List[MedalTypeGQLModel] = strawberry.field(
        description="""Get a page of MedalTypes""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[MedalTypeGQLModel](whereType=MedalTypeInputFilter)
    )

from uoishelpers.resolvers import TreeInputStructureMixin, InputModelMixin

@strawberry.input(
    description="""Input type for creating a MedalType"""
)
class MedalTypeInsertGQLModel(TreeInputStructureMixin):
    getLoader = MedalTypeGQLModel.getLoader
    
    master_medaltype_id: typing.Optional[IDType] = strawberry.field(
        description="""Parent MedalType id""",
        default=None
    )
    
    name: typing.Optional[str] = strawberry.field(
        description="""MedalType name""",
        default=None
    )
    
    id: typing.Optional[IDType] = strawberry.field(
        description="""MedalType id""",
        default=None
    )
    
    sub_medaltypes: typing.Optional[typing.List["MedalTypeInsertGQLModel"]] = strawberry.field(
        description="Child MedalTypes",
        default_factory=list
    )

    createdby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="""Input type for updating a MedalType"""
)
class MedalTypeUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""MedalType id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="Timestamp of last change"
    )
    name: typing.Optional[str] = strawberry.field(
        description="""MedalType name""",
        default=None
    )
    master_medaltype_id: typing.Optional[IDType] = strawberry.field(
        description="""Parent MedalType id""",
        default=None
    )
    
    changedby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="""Input type for deleting a MedalType"""
)
class MedalTypeDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""MedalType id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""Last change timestamp""",
    )


@strawberry.interface(
    description="""MedalType mutations"""
)
class MedalTypeMutation:
    @strawberry.mutation(
        description="""Insert a MedalType""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleInsertPermission[MedalTypeGQLModel](roles=["administrátor"])
        ]
    )
    async def MedalType_insert(
        self,
        info: strawberry.Info,
        MedalType: MedalTypeInsertGQLModel,
    ) -> typing.Union[MedalTypeGQLModel, InsertError[MedalTypeGQLModel]]:
        return await Insert[MedalTypeGQLModel].DoItSafeWay(info=info, entity=MedalType)
    

    @strawberry.mutation(
        description="""Update a MedalType""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleUpdatePermission[MedalTypeGQLModel](roles=["administrátor"])
        ]
    )
    async def MedalType_update(
        self,
        info: strawberry.Info,
        MedalType: MedalTypeUpdateGQLModel
    ) -> typing.Union[MedalTypeGQLModel, UpdateError[MedalTypeGQLModel]]:
        return await Update[MedalTypeGQLModel].DoItSafeWay(info=info, entity=MedalType)
    

    @strawberry.mutation(
        description="""Delete a MedalType""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleDeletePermission[MedalTypeGQLModel](roles=["administrátor"])
        ]
    )   
    async def MedalType_delete(
        self,
        info: strawberry.Info,
        MedalType: MedalTypeDeleteGQLModel
    ) -> typing.Optional[DeleteError[MedalTypeGQLModel]]:
        return await Delete[MedalTypeGQLModel].DoItSafeWay(info=info, entity=MedalType)