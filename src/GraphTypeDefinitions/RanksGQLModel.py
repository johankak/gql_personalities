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
class RankInputFilter:
    name: str
    path: str
    level: int
    id: IDType
    parent_id: IDType

@strawberry.federation.type(
    description="""Entity representing a Rank (military/organizational rank)""",
    keys=["id"]
)
class RankGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).RankModel

    

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""Rank name""",
        permission_classes=[OnlyForAuthentized]
    )

    
    


@strawberry.interface(
    description="""Rank queries"""
)
class RankQuery:
    rank_by_id: typing.Optional[RankGQLModel] = strawberry.field(
        description="""Get a rank by its id""",
        permission_classes=[OnlyForAuthentized],
        resolver=RankGQLModel.load_with_loader
    )

    rank_page: typing.List[RankGQLModel] = strawberry.field(
        description="""Get a page of ranks""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[RankGQLModel](whereType=RankInputFilter)
    )

from uoishelpers.resolvers import TreeInputStructureMixin, InputModelMixin

@strawberry.input(
    description="""Input type for creating a Rank"""
)
class RankInsertGQLModel(TreeInputStructureMixin):
    getLoader = RankGQLModel.getLoader
    
    parent_id: typing.Optional[IDType] = strawberry.field(
        description="""Parent rank id""",
        default=None
    )
    
    name: typing.Optional[str] = strawberry.field(
        description="""Rank name""",
        default=None
    )
    
    id: typing.Optional[IDType] = strawberry.field(
        description="""Rank id""",
        default=None
    )
    
    children: typing.Optional[typing.List["RankInsertGQLModel"]] = strawberry.field(
        description="Child ranks",
        default_factory=list
    )

    createdby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="""Input type for updating a Rank"""
)
class RankUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""Rank id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="Timestamp of last change"
    )
    name: typing.Optional[str] = strawberry.field(
        description="""Rank name""",
        default=None
    )
    parent_id: typing.Optional[IDType] = strawberry.field(
        description="""Parent rank id""",
        default=None
    )
    
    changedby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="""Input type for deleting a Rank"""
)
class RankDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""Rank id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""Last change timestamp""",
    )


@strawberry.interface(
    description="""Rank mutations"""
)
class RankMutation:
    @strawberry.mutation(
        description="""Insert a Rank""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleInsertPermission[RankGQLModel](roles=["administrátor"])
        ]
    )
    async def rank_insert(
        self,
        info: strawberry.Info,
        rank: RankInsertGQLModel,
    ) -> typing.Union[RankGQLModel, InsertError[RankGQLModel]]:
        return await Insert[RankGQLModel].DoItSafeWay(info=info, entity=rank)
    

    @strawberry.mutation(
        description="""Update a Rank""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleUpdatePermission[RankGQLModel](roles=["administrátor"])
        ]
    )
    async def rank_update(
        self,
        info: strawberry.Info,
        rank: RankUpdateGQLModel
    ) -> typing.Union[RankGQLModel, UpdateError[RankGQLModel]]:
        return await Update[RankGQLModel].DoItSafeWay(info=info, entity=rank)
    

    @strawberry.mutation(
        description="""Delete a Rank""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleDeletePermission[RankGQLModel](roles=["administrátor"])
        ]
    )   
    async def rank_delete(
        self,
        info: strawberry.Info,
        rank: RankDeleteGQLModel
    ) -> typing.Optional[DeleteError[RankGQLModel]]:
        return await Delete[RankGQLModel].DoItSafeWay(info=info, entity=rank)