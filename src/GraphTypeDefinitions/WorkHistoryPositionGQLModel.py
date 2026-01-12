import asyncio
import dataclasses
import datetime
import typing
import strawberry

import strawberry.types
from uoishelpers.gqlpermissions import (
    OnlyForAuthentized
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
WorkHistoryPositionGQLModel = typing.Annotated["WorkHistoryPositionGQLModel", strawberry.lazy(".WorkHistoryPositionGQLModel")]

@createInputs2
class WorkHistoryPositionInputFilter:
    name: str
    path: str
    level: int
    id: IDType
    master_workhistoryposition_id: IDType

@strawberry.federation.type(
    description="""Entity representing a WorkHistoryPosition""",
    keys=["id"]
)
class WorkHistoryPositionGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).WorkHistoryPositionModel

    path: typing.Optional[str] = strawberry.field(
        description="""Materialized path representing the hierarchy location.""",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""WorkHistoryPosition name""",
        permission_classes=[OnlyForAuthentized]
    )

    master_workhistoryposition_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="""Parent position ID (master_workhistoryposition_id)""",
        permission_classes=[OnlyForAuthentized]
    )

    master_workhistoryposition: typing.Optional["WorkHistoryPositionGQLModel"] = strawberry.field(
        description="""Parent WorkHistoryPosition""",
        permission_classes=[OnlyForAuthentized],
        resolver=ScalarResolver["WorkHistoryPositionGQLModel"](fkey_field_name="master_workhistoryposition_id")
    )

    sub_workhistorypositions: typing.List["WorkHistoryPositionGQLModel"] = strawberry.field(
        description="""Child WorkHistoryPositions (sub-positions)""",
        permission_classes=[OnlyForAuthentized],
        resolver=VectorResolver["WorkHistoryPositionGQLModel"](fkey_field_name="master_workhistoryposition_id", whereType=WorkHistoryPositionInputFilter)
    )

@strawberry.interface(
    description="""WorkHistoryPosition queries"""
)
class WorkHistoryPositionQuery:
    WorkHistoryPosition_by_id: typing.Optional[WorkHistoryPositionGQLModel] = strawberry.field(
        description="""Get a WorkHistoryPosition by its id""",
        permission_classes=[OnlyForAuthentized],
        resolver=WorkHistoryPositionGQLModel.load_with_loader
    )

    WorkHistoryPosition_page: typing.List[WorkHistoryPositionGQLModel] = strawberry.field(
        description="""Get a page of WorkHistoryPositions""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[WorkHistoryPositionGQLModel](whereType=WorkHistoryPositionInputFilter)
    )

from uoishelpers.resolvers import TreeInputStructureMixin, InputModelMixin

@strawberry.input(
    description="""Input type for creating a WorkHistoryPosition"""
)
class WorkHistoryPositionInsertGQLModel(TreeInputStructureMixin):
    getLoader = WorkHistoryPositionGQLModel.getLoader
    
    master_workhistoryposition_id: typing.Optional[IDType] = strawberry.field(
        description="""Parent WorkHistoryPosition id""",
        default=None
    )
    
    name: typing.Optional[str] = strawberry.field(
        description="""WorkHistoryPosition name""",
        default=None
    )
    
    id: typing.Optional[IDType] = strawberry.field(
        description="""WorkHistoryPosition id""",
        default=None
    )
    
    # Rekurzivní vkládání dětí
    sub_workhistorypositions: typing.Optional[typing.List["WorkHistoryPositionInsertGQLModel"]] = strawberry.field(
        description="Child WorkHistoryPositions",
        default_factory=list
    )

    createdby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="""Input type for updating a WorkHistoryPosition"""
)
class WorkHistoryPositionUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""WorkHistoryPosition id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="Timestamp of last change"
    )
    name: typing.Optional[str] = strawberry.field(
        description="""WorkHistoryPosition name""",
        default=None
    )
    master_workhistoryposition_id: typing.Optional[IDType] = strawberry.field(
        description="""Parent WorkHistoryPosition id""",
        default=None
    )
    
    changedby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="""Input type for deleting a WorkHistoryPosition"""
)
class WorkHistoryPositionDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""WorkHistoryPosition id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""Last change timestamp""",
    )


@strawberry.interface(
    description="""WorkHistoryPosition mutations"""
)
class WorkHistoryPositionMutation:
    @strawberry.mutation(
        description="""Insert a WorkHistoryPosition""",
        permission_classes=[OnlyForAuthentized],
        extensions=[
            UserAbsoluteAccessControlExtension(roles=["administrátor"])
        ]
    )
    async def WorkHistoryPosition_insert(
        self,
        info: strawberry.Info,
        WorkHistoryPosition: WorkHistoryPositionInsertGQLModel,
        user_roles: typing.List[typing.Any] = None
    ) -> typing.Union[WorkHistoryPositionGQLModel, InsertError[WorkHistoryPositionGQLModel]]:
        return await Insert[WorkHistoryPositionGQLModel].DoItSafeWay(info=info, entity=WorkHistoryPosition)
    

    @strawberry.mutation(
        description="""Update a WorkHistoryPosition""",
        permission_classes=[OnlyForAuthentized],
        extensions=[
            UserAbsoluteAccessControlExtension(roles=["administrátor"])
        ]
    )
    async def WorkHistoryPosition_update(
        self,
        info: strawberry.Info,
        WorkHistoryPosition: WorkHistoryPositionUpdateGQLModel,
        user_roles: typing.List[typing.Any] = None
    ) -> typing.Union[WorkHistoryPositionGQLModel, UpdateError[WorkHistoryPositionGQLModel]]:
        return await Update[WorkHistoryPositionGQLModel].DoItSafeWay(info=info, entity=WorkHistoryPosition)
    

    @strawberry.mutation(
        description="""Delete a WorkHistoryPosition""",
        permission_classes=[OnlyForAuthentized],
        extensions=[
            UserAbsoluteAccessControlExtension(roles=["administrátor"])
        ]
    )   
    async def WorkHistoryPosition_delete(
        self,
        info: strawberry.Info,
        WorkHistoryPosition: WorkHistoryPositionDeleteGQLModel,
        user_roles: typing.List[typing.Any] = None
    ) -> typing.Optional[DeleteError[WorkHistoryPositionGQLModel]]:
        return await Delete[WorkHistoryPositionGQLModel].DoItSafeWay(info=info, entity=WorkHistoryPosition)