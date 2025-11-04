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
class CertificateCategoryInputFilter:
    name: str
    path: str
    level: int
    id: IDType
    parent_id: IDType

@strawberry.federation.type(
    description="""Entity representing a CertificateCategory""",
    keys=["id"]
)
class CertificateCategoryGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).CertificateCategoryModel

    

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""CertificateCategory name""",
        permission_classes=[OnlyForAuthentized]
    )

    
    


@strawberry.interface(
    description="""CertificateCategory queries"""
)
class CertificateCategoryQuery:
    CertificateCategory_by_id: typing.Optional[CertificateCategoryGQLModel] = strawberry.field(
        description="""Get a CertificateCategory by its id""",
        permission_classes=[OnlyForAuthentized],
        resolver=CertificateCategoryGQLModel.load_with_loader
    )

    CertificateCategory_page: typing.List[CertificateCategoryGQLModel] = strawberry.field(
        description="""Get a page of CertificateCategorys""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[CertificateCategoryGQLModel](whereType=CertificateCategoryInputFilter)
    )

from uoishelpers.resolvers import TreeInputStructureMixin, InputModelMixin

@strawberry.input(
    description="""Input type for creating a CertificateCategory"""
)
class CertificateCategoryInsertGQLModel(TreeInputStructureMixin):
    getLoader = CertificateCategoryGQLModel.getLoader
    
    parent_id: typing.Optional[IDType] = strawberry.field(
        description="""Parent CertificateCategory id""",
        default=None
    )
    
    name: typing.Optional[str] = strawberry.field(
        description="""CertificateCategory name""",
        default=None
    )
    
    id: typing.Optional[IDType] = strawberry.field(
        description="""CertificateCategory id""",
        default=None
    )
    
    children: typing.Optional[typing.List["CertificateCategoryInsertGQLModel"]] = strawberry.field(
        description="Child CertificateCategorys",
        default_factory=list
    )

    createdby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="""Input type for updating a CertificateCategory"""
)
class CertificateCategoryUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""CertificateCategory id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="Timestamp of last change"
    )
    name: typing.Optional[str] = strawberry.field(
        description="""CertificateCategory name""",
        default=None
    )
    parent_id: typing.Optional[IDType] = strawberry.field(
        description="""Parent CertificateCategory id""",
        default=None
    )
    
    changedby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="""Input type for deleting a CertificateCategory"""
)
class CertificateCategoryDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""CertificateCategory id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""Last change timestamp""",
    )


@strawberry.interface(
    description="""CertificateCategory mutations"""
)
class CertificateCategoryMutation:
    @strawberry.mutation(
        description="""Insert a CertificateCategory""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleInsertPermission[CertificateCategoryGQLModel](roles=["administrátor"])
        ]
    )
    async def CertificateCategory_insert(
        self,
        info: strawberry.Info,
        CertificateCategory: CertificateCategoryInsertGQLModel,
    ) -> typing.Union[CertificateCategoryGQLModel, InsertError[CertificateCategoryGQLModel]]:
        return await Insert[CertificateCategoryGQLModel].DoItSafeWay(info=info, entity=CertificateCategory)
    

    @strawberry.mutation(
        description="""Update a CertificateCategory""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleUpdatePermission[CertificateCategoryGQLModel](roles=["administrátor"])
        ]
    )
    async def CertificateCategory_update(
        self,
        info: strawberry.Info,
        CertificateCategory: CertificateCategoryUpdateGQLModel
    ) -> typing.Union[CertificateCategoryGQLModel, UpdateError[CertificateCategoryGQLModel]]:
        return await Update[CertificateCategoryGQLModel].DoItSafeWay(info=info, entity=CertificateCategory)
    

    @strawberry.mutation(
        description="""Delete a CertificateCategory""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleDeletePermission[CertificateCategoryGQLModel](roles=["administrátor"])
        ]
    )   
    async def CertificateCategory_delete(
        self,
        info: strawberry.Info,
        CertificateCategory: CertificateCategoryDeleteGQLModel
    ) -> typing.Optional[DeleteError[CertificateCategoryGQLModel]]:
        return await Delete[CertificateCategoryGQLModel].DoItSafeWay(info=info, entity=CertificateCategory)