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


WorkHistoryPositionGQLModel = typing.Annotated["WorkHistoryPositionGQLModel", strawberry.lazy(".WorkHistoryPositionGQLModel")]
WorkHistoryPositionInputFilter = typing.Annotated["WorkHistoryPositionInputFilter", strawberry.lazy(".WorkHistoryPositionGQLModel")]
UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".UserGQLModel")]

@createInputs2
class UserWorkHistoryPositionInputFilter:
    id: IDType
    workhistoryposition_id: IDType
    user_id: IDType
    startdate: datetime.datetime
    enddate: datetime.datetime

    workhistoryposition: WorkHistoryPositionInputFilter = strawberry.field(description="""WorkHistoryPosition filter operators, 
for field "WorkHistoryPosition" the filters could be
{"WorkHistoryPosition": {"name": {"_eq": "Captain"}}}
{"WorkHistoryPosition": {"level": {"_ge": 5}}}
{"WorkHistoryPosition": {"_and": [{"name": {"_like": "Gen%"}}, {"level": {"_ge": 8}}]}}
""")

@strawberry.federation.type(
    keys=["id"], description="""Entity representing assignment of a WorkHistoryPosition to a User with time validity"""
)
class UserWorkHistoryPositionGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).UserWorkHistoryPositionModel
    workhistoryposition_id: typing.Optional[IDType] = strawberry.field(
        description="""WorkHistoryPosition assigned to the user""",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    user_id: typing.Optional[IDType] = strawberry.field( 
        description="""User assigned the WorkHistoryPosition""",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    startdate: typing.Optional[datetime.datetime] = strawberry.field(
        description="""Start date of WorkHistoryPosition validity""",
        default=None,
        permission_classes=[
            OnlyForAuthentized  
        ]
    )

    enddate: typing.Optional[datetime.datetime] = strawberry.field(
        description="""End date of WorkHistoryPosition validity""",
        default=None,
        permission_classes=[
            OnlyForAuthentized  
        ]
    )

    workhistoryposition: typing.Optional[WorkHistoryPositionGQLModel] = strawberry.field(
        description="""WorkHistoryPosition assigned to the user""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[WorkHistoryPositionGQLModel](fkey_field_name="workhistoryposition_id")
    )

    user: typing.Optional[UserGQLModel] = strawberry.field(
        description="""User assigned the WorkHistoryPosition""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[UserGQLModel](fkey_field_name="user_id")
    )

    @strawberry.field(
        description="""Check if the WorkHistoryPosition assignment is currently valid""",
        permission_classes=[OnlyForAuthentized]
    )
    def is_valid(self) -> bool:
        """Returns True if the WorkHistoryPosition is currently valid based on start and end dates"""
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

@strawberry.type(description="Query operations for UserWorkHistoryPosition")
class UserWorkHistoryPositionQuery:

    user_workhistoryposition_by_id: typing.Optional[UserWorkHistoryPositionGQLModel] = strawberry.field(
        description="User WorkHistoryPosition assignment by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=UserWorkHistoryPositionGQLModel.load_with_loader
    )

    user_workhistoryposition_page: typing.List[UserWorkHistoryPositionGQLModel] = strawberry.field(
        description="Selected user WorkHistoryPosition assignments",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[UserWorkHistoryPositionGQLModel](whereType=UserWorkHistoryPositionInputFilter)
    )


from uoishelpers.resolvers import InputModelMixin
@strawberry.input(
    description="""UserWorkHistoryPosition insert mutation"""
)
class UserWorkHistoryPositionInsertGQLModel(InputModelMixin):
    getLoader = UserWorkHistoryPositionGQLModel.getLoader

    workhistoryposition_id: IDType = strawberry.field(
        description="WorkHistoryPosition id to assign",
    )

    user_id: IDType = strawberry.field(
        description="User id who receives the WorkHistoryPosition",
    )

    startdate: typing.Optional[datetime.datetime] = strawberry.field(
        description="Start date of WorkHistoryPosition validity",
        default=None
    )

    enddate: typing.Optional[datetime.datetime] = strawberry.field(
        description="End date of WorkHistoryPosition validity",
        default=None
    )

    id: typing.Optional[IDType] = strawberry.field(
        description="""Client generated id""",
        default=None,
    )

    createdby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="""UserWorkHistoryPosition update mutation"""
)
class UserWorkHistoryPositionUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""Id"""
    )

    lastchange: datetime.datetime = strawberry.field(
        description="""Timestamp"""
    )

    startdate: typing.Optional[datetime.datetime] = strawberry.field(
        description="Start date of WorkHistoryPosition validity",
        default=None
    )

    enddate: typing.Optional[datetime.datetime] = strawberry.field(
        description="End date of WorkHistoryPosition validity",
        default=None
    )

    workhistoryposition_id: typing.Optional[IDType] = strawberry.field(
        description="WorkHistoryPosition id to assign",
        default=None
    )

    changedby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="""UserWorkHistoryPosition delete mutation"""
)
class UserWorkHistoryPositionDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""UserWorkHistoryPosition id"""
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""UserWorkHistoryPosition lastchange"""
    )


@strawberry.type(
    description="""UserWorkHistoryPosition mutation"""
)
class UserWorkHistoryPositionMutation:

    @strawberry.mutation(
        description="""Insert a UserWorkHistoryPosition assignment""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleInsertPermission[UserWorkHistoryPositionGQLModel](roles=["administrátor", "personalista"])
        ],
        extensions=[
            UserAccessControlExtension[InsertError, UserWorkHistoryPositionGQLModel](roles=["administrátor", "personalista"]),
            UserRoleProviderExtension[InsertError, UserWorkHistoryPositionGQLModel](),
            RbacInsertProviderExtension[InsertError, UserWorkHistoryPositionGQLModel](rbac_key_name="user_id")
        ]
    )
    async def user_workhistoryposition_insert(
        self,
        info: strawberry.types.Info,
        user_workhistoryposition: UserWorkHistoryPositionInsertGQLModel,
        user_roles: typing.List[str],
        rbacobject_id: typing.Optional[IDType] = None
    ) -> typing.Union[UserWorkHistoryPositionGQLModel, InsertError[UserWorkHistoryPositionGQLModel]]:
        # Validate that startdate is before enddate if both are provided
        if user_workhistoryposition.startdate and user_workhistoryposition.enddate:
            if user_workhistoryposition.startdate >= user_workhistoryposition.enddate:
                return InsertError[UserWorkHistoryPositionGQLModel](
                    msg="Start date must be before end date",
                    code="d5e8f9a2-4b3c-4d5e-9f8a-1b2c3d4e5f6a",
                    location="user_workhistoryposition_insert"
                )

        return await Insert[UserWorkHistoryPositionGQLModel].DoItSafeWay(info=info, entity=user_workhistoryposition)
    

    @strawberry.mutation(
        description="""Update the UserWorkHistoryPosition assignment""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleUpdatePermission[UserWorkHistoryPositionGQLModel](roles=["administrátor", "personalista"])
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, UserWorkHistoryPositionGQLModel](roles=["administrátor"]),
            UserRoleProviderExtension[UpdateError, UserWorkHistoryPositionGQLModel](),
            RbacProviderExtension[UpdateError, UserWorkHistoryPositionGQLModel](),
            LoadDataExtension[UpdateError, UserWorkHistoryPositionGQLModel]()
        ],
    )
    async def user_workhistoryposition_update(
        self,
        info: strawberry.types.Info,
        user_workhistoryposition: UserWorkHistoryPositionUpdateGQLModel,
        db_row: typing.Any,
        user_roles: typing.List[str],
        rbacobject_id: typing.Optional[IDType] = None
    ) -> typing.Union[UserWorkHistoryPositionGQLModel, UpdateError[UserWorkHistoryPositionGQLModel]]:
        # Validate dates if both are being updated
        startdate = user_workhistoryposition.startdate if user_workhistoryposition.startdate is not None else db_row.startdate
        enddate = user_workhistoryposition.enddate if user_workhistoryposition.enddate is not None else db_row.enddate

        if startdate and enddate and startdate >= enddate:
            return UpdateError[UserWorkHistoryPositionGQLModel](
                _entity=db_row,
                msg="Start date must be before end date",
                code="e6f9a3b4-5c4d-5e6f-af9b-2c3d4e5f6a7b",
                location="user_workhistoryposition_update",
                _input=user_workhistoryposition
            )

        return await Update[UserWorkHistoryPositionGQLModel].DoItSafeWay(info=info, entity=user_workhistoryposition)

    @strawberry.mutation(
        description="""Delete a UserWorkHistoryPosition assignment""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleDeletePermission[UserWorkHistoryPositionGQLModel](roles=["administrátor", "personalista"])
        ],
        extensions=[
            UserAccessControlExtension[DeleteError, UserWorkHistoryPositionGQLModel](roles=["administrátor", "personalista"]),
            UserRoleProviderExtension[DeleteError, UserWorkHistoryPositionGQLModel](),
            RbacProviderExtension[DeleteError, UserWorkHistoryPositionGQLModel](),
            LoadDataExtension[DeleteError, UserWorkHistoryPositionGQLModel]()
        ]
    )
    async def user_workhistoryposition_delete(
        self,
        info: strawberry.types.Info,
        user_workhistoryposition: UserWorkHistoryPositionDeleteGQLModel,
        db_row: typing.Any,
        user_roles: typing.List[str],
        rbacobject_id: typing.Optional[IDType] = None
    ) -> typing.Optional[DeleteError[UserWorkHistoryPositionGQLModel]]:
        return await Delete[UserWorkHistoryPositionGQLModel].DoItSafeWay(info=info, entity=user_workhistoryposition)