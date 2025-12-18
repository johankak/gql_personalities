import asyncio
import dataclasses
import datetime
import typing
import strawberry

from uoishelpers.gqlpermissions import (
    OnlyForAuthentized,
    SimpleInsertPermission, 
    SimpleUpdatePermission, 
    SimpleDeletePermission
)    
from uoishelpers.resolvers import (
    getLoadersFromInfo, 
    getUserFromInfo,
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

from .BaseGQLModel import BaseGQLModel, IDType


StudyPlaceGQLModel = typing.Annotated["StudyPlaceGQLModel", strawberry.lazy(".StudyPlaceGQLModel")]
StudyPlaceInputFilter = typing.Annotated["StudyPlaceInputFilter", strawberry.lazy(".StudyPlaceGQLModel")]
UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".UserGQLModel")]

@createInputs2
class UserStudyPlaceInputFilter:
    id: IDType
    studyplace_id: IDType
    user_id: IDType
    startdate: datetime.datetime
    enddate: datetime.datetime

    studyplace: StudyPlaceInputFilter = strawberry.field(description="""StudyPlace filter operators, 
for field "StudyPlace" the filters could be
{"StudyPlace": {"name": {"_eq": "Captain"}}}
{"StudyPlace": {"level": {"_ge": 5}}}
{"StudyPlace": {"_and": [{"name": {"_like": "Gen%"}}, {"level": {"_ge": 8}}]}}
""")

@strawberry.federation.type(
    keys=["id"], description="""Entity representing assignment of a StudyPlace to a User with time validity"""
)
class UserStudyPlaceGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).UserStudyPlaceModel

    studyplace_id: typing.Optional[IDType] = strawberry.field(
        description="""StudyPlace assigned to the user""",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    user_id: typing.Optional[IDType] = strawberry.field( 
        description="""User assigned the StudyPlace""",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    startdate: typing.Optional[datetime.datetime] = strawberry.field(
        description="""Start date of StudyPlace validity""",
        default=None,
        permission_classes=[
            OnlyForAuthentized  
        ]
    )

    enddate: typing.Optional[datetime.datetime] = strawberry.field(
        description="""End date of StudyPlace validity""",
        default=None,
        permission_classes=[
            OnlyForAuthentized  
        ]
    )

    studyplace: typing.Optional[StudyPlaceGQLModel] = strawberry.field(
        description="""StudyPlace assigned to the user""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[StudyPlaceGQLModel](fkey_field_name="studyplace_id")
    )

    user: typing.Optional[UserGQLModel] = strawberry.field(
        description="""User assigned the StudyPlace""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[UserGQLModel](fkey_field_name="user_id")
    )

    @strawberry.field(
        description="""Check if the StudyPlace assignment is currently valid""",
        permission_classes=[OnlyForAuthentized]
    )
    def is_valid(self) -> bool:
        """Returns True if the StudyPlace is currently valid based on start and end dates"""
        now = datetime.datetime.now()
        if self.startdate and self.enddate:
            return self.startdate <= now <= self.enddate
        elif self.startdate:
            return self.startdate <= now
        elif self.enddate:
            return now <= self.enddate
        return True  # No date restrictions means always valid

    user: typing.Optional[UserGQLModel] = strawberry.field(
        description="""User assigned to the invitation""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[UserGQLModel](fkey_field_name="user_id")
    )

@strawberry.type(description="Query operations for UserStudyPlace")
class UserStudyPlaceQuery:

    user_studyplace_by_id: typing.Optional[UserStudyPlaceGQLModel] = strawberry.field(
        description="User StudyPlace assignment by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=UserStudyPlaceGQLModel.load_with_loader
    )

    user_studyplace_page: typing.List[UserStudyPlaceGQLModel] = strawberry.field(
        description="Selected user StudyPlace assignments",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[UserStudyPlaceGQLModel](whereType=UserStudyPlaceInputFilter)
    )


from uoishelpers.resolvers import InputModelMixin
@strawberry.input(
    description="""UserStudyPlace insert mutation"""
)
class UserStudyPlaceInsertGQLModel(InputModelMixin):
    getLoader = UserStudyPlaceGQLModel.getLoader
    
    studyplace_id: IDType = strawberry.field(
        description="StudyPlace id to assign",
    )

    user_id: IDType = strawberry.field(
        description="User id who receives the StudyPlace",
    )

    startdate: typing.Optional[datetime.datetime] = strawberry.field(
        description="Start date of StudyPlace validity",
        default=None
    )

    enddate: typing.Optional[datetime.datetime] = strawberry.field(
        description="End date of StudyPlace validity",
        default=None
    )

    id: typing.Optional[IDType] = strawberry.field(
        description="""Client generated id""",
        default=None,
    )

    createdby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="""UserStudyPlace update mutation"""
)
class UserStudyPlaceUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""Id"""
    )

    lastchange: datetime.datetime = strawberry.field(
        description="""Timestamp"""
    )

    startdate: typing.Optional[datetime.datetime] = strawberry.field(
        description="Start date of StudyPlace validity",
        default=None
    )

    enddate: typing.Optional[datetime.datetime] = strawberry.field(
        description="End date of StudyPlace validity",
        default=None
    )

    studyplace_id: typing.Optional[IDType] = strawberry.field(
        description="StudyPlace id to assign",
        default=None
    )

    changedby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="""UserStudyPlace delete mutation"""
)
class UserStudyPlaceDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""UserStudyPlace id"""
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""UserStudyPlace lastchange"""
    )


@strawberry.type(
    description="""UserStudyPlace mutation"""
)
class UserStudyPlaceMutation:
    
    @strawberry.mutation(
        description="""Insert a UserStudyPlace assignment""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleInsertPermission[UserStudyPlaceGQLModel](roles=["administrátor", "personalista"])
        ],
        extensions=[
            UserAccessControlExtension[InsertError, UserStudyPlaceGQLModel](roles=["administrátor", "personalista"]),
            UserRoleProviderExtension[InsertError, UserStudyPlaceGQLModel](),
            RbacInsertProviderExtension[InsertError, UserStudyPlaceGQLModel](rbac_key_name="user_id")
        ]
    )
    async def user_studyplace_insert(
        self,
        info: strawberry.types.Info,
        user_studyplace: UserStudyPlaceInsertGQLModel,
        user_roles: typing.List[str],
        rbacobject_id: typing.Optional[IDType] = None
    ) -> typing.Union[UserStudyPlaceGQLModel, InsertError[UserStudyPlaceGQLModel]]:
        # Validate that startdate is before enddate if both are provided
        if user_studyplace.startdate and user_studyplace.enddate:
            if user_studyplace.startdate >= user_studyplace.enddate:
                return InsertError[UserStudyPlaceGQLModel](
                    msg="Start date must be before end date",
                    code="d5e8f9a2-4b3c-4d5e-9f8a-1b2c3d4e5f6a",
                    location="user_studyplace_insert"
                )

        return await Insert[UserStudyPlaceGQLModel].DoItSafeWay(info=info, entity=user_studyplace)
    

    @strawberry.mutation(
        description="""Update the UserStudyPlace assignment""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleUpdatePermission[UserStudyPlaceGQLModel](roles=["administrátor", "personalista"])
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, UserStudyPlaceGQLModel](roles=["administrátor"]),
            UserRoleProviderExtension[UpdateError, UserStudyPlaceGQLModel](),
            RbacProviderExtension[UpdateError, UserStudyPlaceGQLModel](),
            LoadDataExtension[UpdateError, UserStudyPlaceGQLModel]()
        ],
    )
    async def user_StudyPlace_update(
        self,
        info: strawberry.types.Info,
        user_studyplace: UserStudyPlaceUpdateGQLModel,
        db_row: typing.Any,
        user_roles: typing.List[str],
        rbacobject_id: typing.Optional[IDType] = None
    ) -> typing.Union[UserStudyPlaceGQLModel, UpdateError[UserStudyPlaceGQLModel]]:
        # Validate dates if both are being updated
        startdate = user_studyplace.startdate if user_studyplace.startdate is not None else db_row.startdate
        enddate = user_studyplace.enddate if user_studyplace.enddate is not None else db_row.enddate

        if startdate and enddate and startdate >= enddate:
            return UpdateError[UserStudyPlaceGQLModel](
                _entity=db_row,
                msg="Start date must be before end date",
                code="e6f9a3b4-5c4d-5e6f-af9b-2c3d4e5f6a7b",
                location="user_studyplace_update",
                _input=user_studyplace
            )

        return await Update[UserStudyPlaceGQLModel].DoItSafeWay(info=info, entity=user_studyplace)

    @strawberry.mutation(
        description="""Delete a UserStudyPlace assignment""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleDeletePermission[UserStudyPlaceGQLModel](roles=["administrátor", "personalista"])
        ],
        extensions=[
            UserAccessControlExtension[DeleteError, UserStudyPlaceGQLModel](roles=["administrátor", "personalista"]),
            UserRoleProviderExtension[DeleteError, UserStudyPlaceGQLModel](),
            RbacProviderExtension[DeleteError, UserStudyPlaceGQLModel](),
            LoadDataExtension[DeleteError, UserStudyPlaceGQLModel]()
        ]
    )
    async def user_StudyPlace_delete(
        self,
        info: strawberry.types.Info,
        user_studyplace: UserStudyPlaceDeleteGQLModel,
        db_row: typing.Any,
        user_roles: typing.List[str],
        rbacobject_id: typing.Optional[IDType] = None
    ) -> typing.Optional[DeleteError[UserStudyPlaceGQLModel]]:
        return await Delete[UserStudyPlaceGQLModel].DoItSafeWay(info=info, entity=user_studyplace)