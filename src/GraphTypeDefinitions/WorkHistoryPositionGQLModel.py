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

@createInputs2
class WorkHistoryPositionInputFilter:
    name: str
    path: str
    level: int
    id: IDType
    parent_id: IDType

@strawberry.federation.type(
    description="""Entity representing a WorkHistoryPosition""",
    keys=["id"]
)
class WorkHistoryPositionGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).WorkHistoryPositionModel

    

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""WorkHistoryPosition name""",
        permission_classes=[OnlyForAuthentized]
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
    
    parent_id: typing.Optional[IDType] = strawberry.field(
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
    
    children: typing.Optional[typing.List["WorkHistoryPositionInsertGQLModel"]] = strawberry.field(
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
    parent_id: typing.Optional[IDType] = strawberry.field(
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
        permission_classes=[
            OnlyForAuthentized,
            SimpleInsertPermission[WorkHistoryPositionGQLModel](roles=["administrátor"])
        ]
    )
    async def WorkHistoryPosition_insert(
        self,
        info: strawberry.Info,
        WorkHistoryPosition: WorkHistoryPositionInsertGQLModel,
    ) -> typing.Union[WorkHistoryPositionGQLModel, InsertError[WorkHistoryPositionGQLModel]]:
        return await Insert[WorkHistoryPositionGQLModel].DoItSafeWay(info=info, entity=WorkHistoryPosition)
    

    @strawberry.mutation(
        description="""Update a WorkHistoryPosition""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleUpdatePermission[WorkHistoryPositionGQLModel](roles=["administrátor"])
        ]
    )
    async def WorkHistoryPosition_update(
        self,
        info: strawberry.Info,
        WorkHistoryPosition: WorkHistoryPositionUpdateGQLModel
    ) -> typing.Union[WorkHistoryPositionGQLModel, UpdateError[WorkHistoryPositionGQLModel]]:
        return await Update[WorkHistoryPositionGQLModel].DoItSafeWay(info=info, entity=WorkHistoryPosition)
    

    @strawberry.mutation(
        description="""Delete a WorkHistoryPosition""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleDeletePermission[WorkHistoryPositionGQLModel](roles=["administrátor"])
        ]
    )   
    async def WorkHistoryPosition_delete(
        self,
        info: strawberry.Info,
        WorkHistoryPosition: WorkHistoryPositionDeleteGQLModel
    ) -> typing.Optional[DeleteError[WorkHistoryPositionGQLModel]]:
        return await Delete[WorkHistoryPositionGQLModel].DoItSafeWay(info=info, entity=WorkHistoryPosition)