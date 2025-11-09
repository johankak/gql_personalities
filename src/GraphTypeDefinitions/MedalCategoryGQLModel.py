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
class MedalCategoryInputFilter:
    name: str
    path: str
    level: int
    id: IDType
    parent_id: IDType

@strawberry.federation.type(
    description="""Entity representing a MedalCategory""",
    keys=["id"]
)
class MedalCategoryGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).MedalCategoryModel

    

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""MedalCategory name""",
        permission_classes=[OnlyForAuthentized]
    )

    
    


@strawberry.interface(
    description="""MedalCategory queries"""
)
class MedalCategoryQuery:
    MedalCategory_by_id: typing.Optional[MedalCategoryGQLModel] = strawberry.field(
        description="""Get a MedalCategory by its id""",
        permission_classes=[OnlyForAuthentized],
        resolver=MedalCategoryGQLModel.load_with_loader
    )

    MedalCategory_page: typing.List[MedalCategoryGQLModel] = strawberry.field(
        description="""Get a page of MedalCategorys""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[MedalCategoryGQLModel](whereType=MedalCategoryInputFilter)
    )

from uoishelpers.resolvers import TreeInputStructureMixin, InputModelMixin

@strawberry.input(
    description="""Input type for creating a MedalCategory"""
)
class MedalCategoryInsertGQLModel(TreeInputStructureMixin):
    getLoader = MedalCategoryGQLModel.getLoader
    
    parent_id: typing.Optional[IDType] = strawberry.field(
        description="""Parent MedalCategory id""",
        default=None
    )
    
    name: typing.Optional[str] = strawberry.field(
        description="""MedalCategory name""",
        default=None
    )
    
    id: typing.Optional[IDType] = strawberry.field(
        description="""MedalCategory id""",
        default=None
    )
    
    children: typing.Optional[typing.List["MedalCategoryInsertGQLModel"]] = strawberry.field(
        description="Child MedalCategorys",
        default_factory=list
    )

    createdby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="""Input type for updating a MedalCategory"""
)
class MedalCategoryUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""MedalCategory id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="Timestamp of last change"
    )
    name: typing.Optional[str] = strawberry.field(
        description="""MedalCategory name""",
        default=None
    )
    parent_id: typing.Optional[IDType] = strawberry.field(
        description="""Parent MedalCategory id""",
        default=None
    )
    
    changedby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="""Input type for deleting a MedalCategory"""
)
class MedalCategoryDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""MedalCategory id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""Last change timestamp""",
    )


@strawberry.interface(
    description="""MedalCategory mutations"""
)
class MedalCategoryMutation:
    @strawberry.mutation(
        description="""Insert a MedalCategory""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleInsertPermission[MedalCategoryGQLModel](roles=["administrátor"])
        ]
    )
    async def MedalCategory_insert(
        self,
        info: strawberry.Info,
        MedalCategory: MedalCategoryInsertGQLModel,
    ) -> typing.Union[MedalCategoryGQLModel, InsertError[MedalCategoryGQLModel]]:
        return await Insert[MedalCategoryGQLModel].DoItSafeWay(info=info, entity=MedalCategory)
    

    @strawberry.mutation(
        description="""Update a MedalCategory""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleUpdatePermission[MedalCategoryGQLModel](roles=["administrátor"])
        ]
    )
    async def MedalCategory_update(
        self,
        info: strawberry.Info,
        MedalCategory: MedalCategoryUpdateGQLModel
    ) -> typing.Union[MedalCategoryGQLModel, UpdateError[MedalCategoryGQLModel]]:
        return await Update[MedalCategoryGQLModel].DoItSafeWay(info=info, entity=MedalCategory)
    

    @strawberry.mutation(
        description="""Delete a MedalCategory""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleDeletePermission[MedalCategoryGQLModel](roles=["administrátor"])
        ]
    )   
    async def MedalCategory_delete(
        self,
        info: strawberry.Info,
        MedalCategory: MedalCategoryDeleteGQLModel
    ) -> typing.Optional[DeleteError[MedalCategoryGQLModel]]:
        return await Delete[MedalCategoryGQLModel].DoItSafeWay(info=info, entity=MedalCategory)