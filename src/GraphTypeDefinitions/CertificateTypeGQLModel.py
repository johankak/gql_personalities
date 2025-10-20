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
class CertificateTypeInputFilter:
    name: str
    path: str
    level: int
    id: IDType
    parent_id: IDType

@strawberry.federation.type(
    description="""Entity representing a CertificateType""",
    keys=["id"]
)
class CertificateTypeGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).CertificateTypeModel

    

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""CertificateType name""",
        permission_classes=[OnlyForAuthentized]
    )

    
    


@strawberry.interface(
    description="""CertificateType queries"""
)
class CertificateTypeQuery:
    CertificateType_by_id: typing.Optional[CertificateTypeGQLModel] = strawberry.field(
        description="""Get a CertificateType by its id""",
        permission_classes=[OnlyForAuthentized],
        resolver=CertificateTypeGQLModel.load_with_loader
    )

    CertificateType_page: typing.List[CertificateTypeGQLModel] = strawberry.field(
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
    
    parent_id: typing.Optional[IDType] = strawberry.field(
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
    
    children: typing.Optional[typing.List["CertificateTypeInsertGQLModel"]] = strawberry.field(
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
    parent_id: typing.Optional[IDType] = strawberry.field(
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
        description="""Insert a CertificateType""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleInsertPermission[CertificateTypeGQLModel](roles=["administrátor"])
        ]
    )
    async def CertificateType_insert(
        self,
        info: strawberry.Info,
        CertificateType: CertificateTypeInsertGQLModel,
    ) -> typing.Union[CertificateTypeGQLModel, InsertError[CertificateTypeGQLModel]]:
        return await Insert[CertificateTypeGQLModel].DoItSafeWay(info=info, entity=CertificateType)
    

    @strawberry.mutation(
        description="""Update a CertificateType""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleUpdatePermission[CertificateTypeGQLModel](roles=["administrátor"])
        ]
    )
    async def CertificateType_update(
        self,
        info: strawberry.Info,
        CertificateType: CertificateTypeUpdateGQLModel
    ) -> typing.Union[CertificateTypeGQLModel, UpdateError[CertificateTypeGQLModel]]:
        return await Update[CertificateTypeGQLModel].DoItSafeWay(info=info, entity=CertificateType)
    

    @strawberry.mutation(
        description="""Delete a CertificateType""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleDeletePermission[CertificateTypeGQLModel](roles=["administrátor"])
        ]
    )   
    async def CertificateType_delete(
        self,
        info: strawberry.Info,
        CertificateType: CertificateTypeDeleteGQLModel
    ) -> typing.Optional[DeleteError[CertificateTypeGQLModel]]:
        return await Delete[CertificateTypeGQLModel].DoItSafeWay(info=info, entity=CertificateType)