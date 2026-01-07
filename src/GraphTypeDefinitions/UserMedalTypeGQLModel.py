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


MedalTypeGQLModel = typing.Annotated["MedalTypeGQLModel", strawberry.lazy(".MedalTypeGQLModel")]
MedalTypeInputFilter = typing.Annotated["MedalTypeInputFilter", strawberry.lazy(".MedalTypeGQLModel")]
UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".UserGQLModel")]

@createInputs2
class UserMedalTypeInputFilter:
    id: IDType
    medaltype_id: IDType
    user_id: IDType
    startdate: datetime.datetime
    enddate: datetime.datetime

    medaltype: MedalTypeInputFilter = strawberry.field(description="""MedalType filter operators,
for field "MedalType" the filters could be
{"MedalType": {"name": {"_eq": "Captain"}}}
{"MedalType": {"level": {"_ge": 5}}}
{"MedalType": {"_and": [{"name": {"_like": "Gen%"}}, {"level": {"_ge": 8}}]}}
""")

@strawberry.federation.type(
    keys=["id"], description="""Entity representing assignment of a MedalType to a User with time validity"""
)
class UserMedalTypeGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).UserMedalTypeModel
    medaltype_id: typing.Optional[IDType] = strawberry.field(
        description="""MedalType assigned to the user""",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    user_id: typing.Optional[IDType] = strawberry.field( 
        description="""User assigned the MedalType""",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    startdate: typing.Optional[datetime.datetime] = strawberry.field(
        description="""Start date of MedalType validity""",
        default=None,
        permission_classes=[
            OnlyForAuthentized  
        ]
    )

    enddate: typing.Optional[datetime.datetime] = strawberry.field(
        description="""End date of MedalType validity""",
        default=None,
        permission_classes=[
            OnlyForAuthentized  
        ]
    )

    medaltype: typing.Optional[MedalTypeGQLModel] = strawberry.field(
        description="""MedalType assigned to the user""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[MedalTypeGQLModel](fkey_field_name="medaltype_id")
    )

    user: typing.Optional[UserGQLModel] = strawberry.field(
        description="""User assigned the MedalType""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[UserGQLModel](fkey_field_name="user_id")
    )

    @strawberry.field(
        description="""Check if the MedalType assignment is currently valid""",
        permission_classes=[OnlyForAuthentized]
    )
    def is_valid(self) -> bool:
        """Returns True if the MedalType is currently valid based on start and end dates"""
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

@strawberry.type(description="Query operations for UserMedalType")
class UserMedalTypeQuery:

    user_medaltype_by_id: typing.Optional[UserMedalTypeGQLModel] = strawberry.field(
        description="User MedalType assignment by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=UserMedalTypeGQLModel.load_with_loader
    )

    user_medaltype_page: typing.List[UserMedalTypeGQLModel] = strawberry.field(
        description="Selected user MedalType assignments",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[UserMedalTypeGQLModel](whereType=UserMedalTypeInputFilter)
    )


from uoishelpers.resolvers import InputModelMixin
@strawberry.input(
    description="""UserMedalType insert mutation"""
)
class UserMedalTypeInsertGQLModel(InputModelMixin):
    getLoader = UserMedalTypeGQLModel.getLoader

    medaltype_id: IDType = strawberry.field(
        description="MedalType id to assign",
    )

    user_id: IDType = strawberry.field(
        description="User id who receives the MedalType",
    )

    startdate: typing.Optional[datetime.datetime] = strawberry.field(
        description="Start date of MedalType validity",
        default=None
    )

    enddate: typing.Optional[datetime.datetime] = strawberry.field(
        description="End date of MedalType validity",
        default=None
    )

    id: typing.Optional[IDType] = strawberry.field(
        description="""Client generated id""",
        default=None,
    )

    createdby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="""UserMedalType update mutation"""
)
class UserMedalTypeUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""Id"""
    )

    lastchange: datetime.datetime = strawberry.field(
        description="""Timestamp"""
    )

    startdate: typing.Optional[datetime.datetime] = strawberry.field(
        description="Start date of MedalType validity",
        default=None
    )

    enddate: typing.Optional[datetime.datetime] = strawberry.field(
        description="End date of MedalType validity",
        default=None
    )

    medaltype_id: typing.Optional[IDType] = strawberry.field(
        description="MedalType id to assign",
        default=None
    )

    changedby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="""UserMedalType delete mutation"""
)
class UserMedalTypeDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""UserMedalType id"""
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""UserMedalType lastchange"""
    )


@strawberry.type(
    description="""UserMedalType mutation"""
)
class UserMedalTypeMutation:

    @strawberry.mutation(
        description="""Insert a UserMedalType assignment""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleInsertPermission[UserMedalTypeGQLModel](roles=["administrátor", "personalista"])
        ],
        extensions=[
            UserAccessControlExtension[InsertError, UserMedalTypeGQLModel](roles=["administrátor", "personalista"]),
            UserRoleProviderExtension[InsertError, UserMedalTypeGQLModel](),
            RbacInsertProviderExtension[InsertError, UserMedalTypeGQLModel](rbac_key_name="user_id")
        ]
    )
    async def user_medal_type_insert(
        self,
        info: strawberry.types.Info,
        user_medal_type: UserMedalTypeInsertGQLModel,
        user_roles: typing.List[str],
        rbacobject_id: typing.Optional[IDType] = None
    ) -> typing.Union[UserMedalTypeGQLModel, InsertError[UserMedalTypeGQLModel]]:
        # Validate that startdate is before enddate if both are provided
        if user_medal_type.startdate and user_medal_type.enddate:
            if user_medal_type.startdate >= user_medal_type.enddate:
                return InsertError[UserMedalTypeGQLModel](
                    msg="Start date must be before end date",
                    code="d5e8f9a2-4b3c-4d5e-9f8a-1b2c3d4e5f6a",
                    location="user_medal_type_insert"
                )

        return await Insert[UserMedalTypeGQLModel].DoItSafeWay(info=info, entity=user_medal_type)
    

    @strawberry.mutation(
        description="""Update the UserMedalType assignment""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleUpdatePermission[UserMedalTypeGQLModel](roles=["administrátor", "personalista"])
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, UserMedalTypeGQLModel](roles=["administrátor"]),
            UserRoleProviderExtension[UpdateError, UserMedalTypeGQLModel](),
            RbacProviderExtension[UpdateError, UserMedalTypeGQLModel](),
            LoadDataExtension[UpdateError, UserMedalTypeGQLModel]()
        ],
    )
    async def user_medal_type_update(
        self,
        info: strawberry.types.Info,
        user_medal_type: UserMedalTypeUpdateGQLModel,
        db_row: typing.Any,
        user_roles: typing.List[str],
        rbacobject_id: typing.Optional[IDType] = None
    ) -> typing.Union[UserMedalTypeGQLModel, UpdateError[UserMedalTypeGQLModel]]:
        # Validate dates if both are being updated
        startdate = user_medal_type.startdate if user_medal_type.startdate is not None else db_row.startdate
        enddate = user_medal_type.enddate if user_medal_type.enddate is not None else db_row.enddate

        if startdate and enddate and startdate >= enddate:
            return UpdateError[UserMedalTypeGQLModel](
                _entity=db_row,
                msg="Start date must be before end date",
                code="e6f9a3b4-5c4d-5e6f-af9b-2c3d4e5f6a7b",
                location="user_medal_type_update",
                _input=user_medal_type
            )

        return await Update[UserMedalTypeGQLModel].DoItSafeWay(info=info, entity=user_medal_type)

    @strawberry.mutation(
        description="""Delete a UserMedalType assignment""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleDeletePermission[UserMedalTypeGQLModel](roles=["administrátor", "personalista"])
        ],
        extensions=[
            UserAccessControlExtension[DeleteError, UserMedalTypeGQLModel](roles=["administrátor", "personalista"]),
            UserRoleProviderExtension[DeleteError, UserMedalTypeGQLModel](),
            RbacProviderExtension[DeleteError, UserMedalTypeGQLModel](),
            LoadDataExtension[DeleteError, UserMedalTypeGQLModel]()
        ]
    )
    async def user_medal_type_delete(
        self,
        info: strawberry.types.Info,
        user_medal_type: UserMedalTypeDeleteGQLModel,
        db_row: typing.Any,
        user_roles: typing.List[str],
        rbacobject_id: typing.Optional[IDType] = None
    ) -> typing.Optional[DeleteError[UserMedalTypeGQLModel]]:
        return await Delete[UserMedalTypeGQLModel].DoItSafeWay(info=info, entity=user_medal_type)