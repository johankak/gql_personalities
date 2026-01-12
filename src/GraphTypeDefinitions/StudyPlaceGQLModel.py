import asyncio
import dataclasses
import datetime
import typing
import strawberry

import strawberry.types
from uoishelpers.gqlpermissions import (
    OnlyForAuthentized,
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
StudyPlaceGQLModel = typing.Annotated["StudyPlaceGQLModel", strawberry.lazy(".StudyPlaceGQLModel")]

@createInputs2
class StudyPlaceInputFilter:
    name: str
    path: str
    level: int
    id: IDType
    master_studyplace_id: IDType

@strawberry.federation.type(
    description="""Entity representing a StudyPlace""",
    keys=["id"]
)
class StudyPlaceGQLModel(BaseGQLModel):
    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).StudyPlaceModel

    path: typing.Optional[str] = strawberry.field(
        description="""Materialized path representing the hierarchy location.""",
        default=None,
        permission_classes=[OnlyForAuthentized]
    )

    name: typing.Optional[str] = strawberry.field(
        default=None,
        description="""StudyPlace name""",
        permission_classes=[OnlyForAuthentized]
    )

    master_studyplace_id: typing.Optional[IDType] = strawberry.field(
        default=None,
        description="""Parent StudyPlace ID""",
        permission_classes=[OnlyForAuthentized]
    )

    master_studyplace: typing.Optional["StudyPlaceGQLModel"] = strawberry.field(
        description="""Parent StudyPlace""",
        permission_classes=[OnlyForAuthentized],
        resolver=ScalarResolver["StudyPlaceGQLModel"](fkey_field_name="master_studyplace_id")
    )

    sub_studyplaces: typing.List["StudyPlaceGQLModel"] = strawberry.field(
        description="""Child StudyPlaces""",
        permission_classes=[OnlyForAuthentized],
        resolver=VectorResolver["StudyPlaceGQLModel"](fkey_field_name="master_studyplace_id", whereType=StudyPlaceInputFilter)
    )

@strawberry.interface(
    description="""StudyPlace queries"""
)
class StudyPlaceQuery:
    StudyPlace_by_id: typing.Optional[StudyPlaceGQLModel] = strawberry.field(
        description="""Get a StudyPlace by its id""",
        permission_classes=[OnlyForAuthentized],
        resolver=StudyPlaceGQLModel.load_with_loader
    )

    StudyPlace_page: typing.List[StudyPlaceGQLModel] = strawberry.field(
        description="""Get a page of StudyPlaces""",
        permission_classes=[OnlyForAuthentized],
        resolver=PageResolver[StudyPlaceGQLModel](whereType=StudyPlaceInputFilter)
    )

from uoishelpers.resolvers import TreeInputStructureMixin, InputModelMixin

@strawberry.input(
    description="""Input type for creating a StudyPlace"""
)
class StudyPlaceInsertGQLModel(TreeInputStructureMixin):
    getLoader = StudyPlaceGQLModel.getLoader
    
    master_studyplace_id: typing.Optional[IDType] = strawberry.field(
        description="""Parent StudyPlace id""",
        default=None
    )
    
    name: typing.Optional[str] = strawberry.field(
        description="""StudyPlace name""",
        default=None
    )
    
    id: typing.Optional[IDType] = strawberry.field(
        description="""StudyPlace id""",
        default=None
    )
    
    sub_studyplaces: typing.Optional[typing.List["StudyPlaceInsertGQLModel"]] = strawberry.field(
        description="Child StudyPlaces",
        default_factory=list
    )

    createdby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="""Input type for updating a StudyPlace"""
)
class StudyPlaceUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""StudyPlace id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="Timestamp of last change"
    )
    name: typing.Optional[str] = strawberry.field(
        description="""StudyPlace name""",
        default=None
    )
    master_studyplace_id: typing.Optional[IDType] = strawberry.field(
        description="""Parent StudyPlace id""",
        default=None
    )
    
    changedby_id: strawberry.Private[IDType] = None


@strawberry.input(
    description="""Input type for deleting a StudyPlace"""
)
class StudyPlaceDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""StudyPlace id""",
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""Last change timestamp""",
    )


@strawberry.interface(
    description="""StudyPlace mutations"""
)
class StudyPlaceMutation:
    @strawberry.mutation(
        description="""Insert a StudyPlace""",
        permission_classes=[OnlyForAuthentized],
        extensions=[
            UserAbsoluteAccessControlExtension(roles=["administrátor"])
        ]
    )
    async def StudyPlace_insert(
        self,
        info: strawberry.Info,
        StudyPlace: StudyPlaceInsertGQLModel,
        user_roles: typing.List[typing.Any] = None
    ) -> typing.Union[StudyPlaceGQLModel, InsertError[StudyPlaceGQLModel]]:
        return await Insert[StudyPlaceGQLModel].DoItSafeWay(info=info, entity=StudyPlace)
    

    @strawberry.mutation(
        description="""Update a StudyPlace""",
        permission_classes=[OnlyForAuthentized],
        extensions=[
            UserAbsoluteAccessControlExtension(roles=["administrátor"])
        ]
    )
    async def StudyPlace_update(
        self,
        info: strawberry.Info,
        StudyPlace: StudyPlaceUpdateGQLModel,
        user_roles: typing.List[typing.Any] = None
    ) -> typing.Union[StudyPlaceGQLModel, UpdateError[StudyPlaceGQLModel]]:
        return await Update[StudyPlaceGQLModel].DoItSafeWay(info=info, entity=StudyPlace)
    

    @strawberry.mutation(
        description="""Delete a StudyPlace""",
        permission_classes=[OnlyForAuthentized],
        extensions=[
            UserAbsoluteAccessControlExtension(roles=["administrátor"])
        ]
    )   
    async def StudyPlace_delete(
        self,
        info: strawberry.Info,
        StudyPlace: StudyPlaceDeleteGQLModel,
        user_roles: typing.List[typing.Any] = None
    ) -> typing.Optional[DeleteError[StudyPlaceGQLModel]]:
        return await Delete[StudyPlaceGQLModel].DoItSafeWay(info=info, entity=StudyPlace)