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


RankGQLModel = typing.Annotated["RankGQLModel", strawberry.lazy(".RankGQLModel")]
RankInputFilter = typing.Annotated["RankInputFilter", strawberry.lazy(".RankGQLModel")]
UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".UserGQLModel")]

@createInputs2
class UserRankInputFilter:
    id: IDType
    rank_id: IDType
    user_id: IDType
    startdate: datetime.datetime
    enddate: datetime.datetime

    rank: RankInputFilter = strawberry.field(description="""Rank filter operators, 
for field "rank" the filters could be
{"rank": {"name": {"_eq": "Captain"}}}
{"rank": {"level": {"_ge": 5}}}
{"rank": {"_and": [{"name": {"_like": "Gen%"}}, {"level": {"_ge": 8}}]}}
""")

@strawberry.federation.type(
    keys=["id"], description="""Entity representing assignment of a Rank to a User with time validity"""
)
class UserRankGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).UserRankModel

    rank_id: typing.Optional[IDType] = strawberry.field(
        description="""Rank assigned to the user""",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    user_id: typing.Optional[IDType] = strawberry.field( 
        description="""User assigned the rank""",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    startdate: typing.Optional[datetime.datetime] = strawberry.field(
        description="""Start date of rank validity""",
        default=None,
        permission_classes=[
            OnlyForAuthentized  
        ]
    )

    enddate: typing.Optional[datetime.datetime] = strawberry.field(
        description="""End date of rank validity""",
        default=None,
        permission_classes=[
            OnlyForAuthentized  
        ]
    )

    rank: typing.Optional[RankGQLModel] = strawberry.field(
        description="""Rank assigned to the user""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[RankGQLModel](fkey_field_name="rank_id")
    )

    user: typing.Optional[UserGQLModel] = strawberry.field(
        description="""User assigned the rank""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[UserGQLModel](fkey_field_name="user_id")
    )

    @strawberry.field(
        description="""Check if the rank assignment is currently valid""",
        permission_classes=[OnlyForAuthentized]
    )
    def is_valid(self) -> bool:
        """Returns True if the rank is currently valid based on start and end dates"""
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

@strawberry.type(description="Query operations for UserRank")
class UserRankQuery:

    user_rank_by_id: typing.Optional[UserRankGQLModel] = strawberry.field(
        description="User rank assignment by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=UserRankGQLModel.load_with_loader
    )

    user_rank_page: typing.List[UserRankGQLModel] = strawberry.field(
        description="Selected user rank assignments",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[UserRankGQLModel](whereType=UserRankInputFilter)
    )


from uoishelpers.resolvers import InputModelMixin
@strawberry.input(
    description="""UserRank insert mutation"""
)
class UserRankInsertGQLModel(InputModelMixin):
    getLoader = UserRankGQLModel.getLoader
    
    rank_id: IDType = strawberry.field(
        description="Rank id to assign",
    )

    user_id: IDType = strawberry.field(
        description="User id who receives the rank",
    )

    startdate: typing.Optional[datetime.datetime] = strawberry.field(
        description="Start date of rank validity",
        default=None
    )

    enddate: typing.Optional[datetime.datetime] = strawberry.field(
        description="End date of rank validity",
        default=None
    )

    id: typing.Optional[IDType] = strawberry.field(
        description="""Client generated id""",
        default=None,
    )

    createdby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="""UserRank update mutation"""
)
class UserRankUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""Id"""
    )

    lastchange: datetime.datetime = strawberry.field(
        description="""Timestamp"""
    )

    startdate: typing.Optional[datetime.datetime] = strawberry.field(
        description="Start date of rank validity",
        default=None
    )

    enddate: typing.Optional[datetime.datetime] = strawberry.field(
        description="End date of rank validity",
        default=None
    )

    rank_id: typing.Optional[IDType] = strawberry.field(
        description="Rank id to assign",
        default=None
    )

    changedby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="""UserRank delete mutation"""
)
class UserRankDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""UserRank id"""
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""UserRank lastchange"""
    )


@strawberry.type(
    description="""UserRank mutation"""
)
class UserRankMutation:
    
    @strawberry.mutation(
        description="""Insert a UserRank assignment""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleInsertPermission[UserRankGQLModel](roles=["administrátor", "personalista"])
        ]
    )
    async def user_rank_insert(
        self,
        info: strawberry.types.Info,
        user_rank: UserRankInsertGQLModel,
    ) -> typing.Union[UserRankGQLModel, InsertError[UserRankGQLModel]]:
        # Validate that startdate is before enddate if both are provided
        if user_rank.startdate and user_rank.enddate:
            if user_rank.startdate >= user_rank.enddate:
                return InsertError[UserRankGQLModel](
                    msg="Start date must be before end date",
                    code="d5e8f9a2-4b3c-4d5e-9f8a-1b2c3d4e5f6a",
                    location="user_rank_insert"
                )
        
        return await Insert[UserRankGQLModel].DoItSafeWay(info=info, entity=user_rank)
    

    @strawberry.mutation(
        description="""Update the UserRank assignment""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleUpdatePermission[UserRankGQLModel](roles=["administrátor", "personalista"])
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, UserRankGQLModel](roles=["administrátor"]),
            UserRoleProviderExtension[UpdateError, UserRankGQLModel](),
            RbacProviderExtension[UpdateError, UserRankGQLModel](),
            LoadDataExtension[UpdateError, UserRankGQLModel]()
        ],
    )
    async def user_rank_update(
        self,
        info: strawberry.types.Info,
        user_rank: UserRankUpdateGQLModel,
        db_row: typing.Any,
        user_roles: typing.List[str],
        rbacobject_id: typing.Optional[IDType] = None
    ) -> typing.Union[UserRankGQLModel, UpdateError[UserRankGQLModel]]:
        # Validate dates if both are being updated
        startdate = user_rank.startdate if user_rank.startdate is not None else db_row.startdate
        enddate = user_rank.enddate if user_rank.enddate is not None else db_row.enddate
        
        if startdate and enddate and startdate >= enddate:
            return UpdateError[UserRankGQLModel](
                _entity=db_row,
                msg="Start date must be before end date",
                code="e6f9a3b4-5c4d-5e6f-af9b-2c3d4e5f6a7b",
                location="user_rank_update",
                _input=user_rank
            )
        
        return await Update[UserRankGQLModel].DoItSafeWay(info=info, entity=user_rank)


    @strawberry.mutation(
        description="""Delete a UserRank assignment""",
        permission_classes=[
            OnlyForAuthentized,
            SimpleDeletePermission[UserRankGQLModel](roles=["administrátor", "personalista"])
        ]
    )
    async def user_rank_delete(
        self,
        info: strawberry.types.Info,
        user_rank: UserRankDeleteGQLModel
    ) -> typing.Optional[DeleteError[UserRankGQLModel]]:
        return await Delete[UserRankGQLModel].DoItSafeWay(info=info, entity=user_rank)