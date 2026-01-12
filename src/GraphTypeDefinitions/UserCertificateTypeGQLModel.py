import asyncio
import dataclasses
import datetime
import typing
import strawberry

from uoishelpers.gqlpermissions import (
    OnlyForAuthentized
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


CertificateTypeGQLModel = typing.Annotated["CertificateTypeGQLModel", strawberry.lazy(".CertificateTypeGQLModel")]
CertificateTypeInputFilter = typing.Annotated["CertificateTypeInputFilter", strawberry.lazy(".CertificateTypeGQLModel")]
UserGQLModel = typing.Annotated["UserGQLModel", strawberry.lazy(".UserGQLModel")]

@createInputs2
class UserCertificateTypeInputFilter:
    id: IDType
    certificate_type_id: IDType
    user_id: IDType
    startdate: datetime.datetime
    enddate: datetime.datetime

    certificate_type: CertificateTypeInputFilter = strawberry.field(description="""CertificateType filter operators, 
for field "CertificateType" the filters could be
{"CertificateType": {"name": {"_eq": "Captain"}}}
{"CertificateType": {"level": {"_ge": 5}}}
{"CertificateType": {"_and": [{"name": {"_like": "Gen%"}}, {"level": {"_ge": 8}}]}}
""")

@strawberry.federation.type(
    keys=["id"], description="""Entity representing assignment of a CertificateType to a User with time validity"""
)
class UserCertificateTypeGQLModel(BaseGQLModel):

    @classmethod
    def getLoader(cls, info: strawberry.types.Info):
        return getLoadersFromInfo(info).UserCertificateTypeModel
    certificate_type_id: typing.Optional[IDType] = strawberry.field(
        description="""CertificateType assigned to the user""",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    user_id: typing.Optional[IDType] = strawberry.field( 
        description="""User assigned the CertificateType""",
        default=None,
        permission_classes=[
            OnlyForAuthentized
        ]
    )

    startdate: typing.Optional[datetime.datetime] = strawberry.field(
        description="""Start date of CertificateType validity""",
        default=None,
        permission_classes=[
            OnlyForAuthentized  
        ]
    )

    enddate: typing.Optional[datetime.datetime] = strawberry.field(
        description="""End date of CertificateType validity""",
        default=None,
        permission_classes=[
            OnlyForAuthentized  
        ]
    )

    certificate_type: typing.Optional[CertificateTypeGQLModel] = strawberry.field(
        description="""CertificateType assigned to the user""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[CertificateTypeGQLModel](fkey_field_name="certificate_type_id")
    )

    user: typing.Optional[UserGQLModel] = strawberry.field(
        description="""User assigned the CertificateType""",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=ScalarResolver[UserGQLModel](fkey_field_name="user_id")
    )

    @strawberry.field(
        description="""Check if the CertificateType assignment is currently valid""",
        permission_classes=[OnlyForAuthentized]
    )
    def is_valid(self) -> bool:
        """Returns True if the CertificateType is currently valid based on start and end dates"""
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

@strawberry.type(description="Query operations for UserCertificateType")
class UserCertificateTypeQuery:

    user_certificatetype_by_id: typing.Optional[UserCertificateTypeGQLModel] = strawberry.field(
        description="User CertificateType assignment by its id",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=UserCertificateTypeGQLModel.load_with_loader
    )

    user_certificate_type_page: typing.List[UserCertificateTypeGQLModel] = strawberry.field(
        description="Selected user CertificateType assignments",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=PageResolver[UserCertificateTypeGQLModel](whereType=UserCertificateTypeInputFilter)
    )


from uoishelpers.resolvers import InputModelMixin
@strawberry.input(
    description="""UserCertificateType insert mutation"""
)
class UserCertificateTypeInsertGQLModel(InputModelMixin):
    getLoader = UserCertificateTypeGQLModel.getLoader

    certificate_type_id: IDType = strawberry.field(
        description="CertificateType id to assign",
    )

    user_id: IDType = strawberry.field(
        description="User id who receives the CertificateType",
    )

    startdate: typing.Optional[datetime.datetime] = strawberry.field(
        description="Start date of CertificateType validity",
        default=None
    )

    enddate: typing.Optional[datetime.datetime] = strawberry.field(
        description="End date of CertificateType validity",
        default=None
    )

    id: typing.Optional[IDType] = strawberry.field(
        description="""Client generated id""",
        default=None,
    )

    createdby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="""UserCertificateType update mutation"""
)
class UserCertificateTypeUpdateGQLModel:
    id: IDType = strawberry.field(
        description="""Id"""
    )

    lastchange: datetime.datetime = strawberry.field(
        description="""Timestamp"""
    )

    startdate: typing.Optional[datetime.datetime] = strawberry.field(
        description="Start date of CertificateType validity",
        default=None
    )

    enddate: typing.Optional[datetime.datetime] = strawberry.field(
        description="End date of CertificateType validity",
        default=None
    )

    certificate_type_id: typing.Optional[IDType] = strawberry.field(
        description="CertificateType id to assign",
        default=None
    )

    changedby_id: strawberry.Private[IDType] = None

@strawberry.input(
    description="""UserCertificateType delete mutation"""
)
class UserCertificateTypeDeleteGQLModel:
    id: IDType = strawberry.field(
        description="""UserCertificateType id"""
    )
    lastchange: datetime.datetime = strawberry.field(
        description="""UserCertificateType lastchange"""
    )


@strawberry.type(
    description="""UserCertificateType mutation"""
)
class UserCertificateTypeMutation:

    @strawberry.mutation(
        description="""Insert a UserCertificateType assignment""",
        permission_classes=[
            OnlyForAuthentized
        ],
        extensions=[
            UserAccessControlExtension[InsertError, UserCertificateTypeGQLModel](roles=["administrátor", "personalista"]),
            UserRoleProviderExtension[InsertError, UserCertificateTypeGQLModel](),
            RbacInsertProviderExtension[InsertError, UserCertificateTypeGQLModel](rbac_key_name="user_id")
        ]
    )
    async def user_certificate_type_insert(
        self,
        info: strawberry.types.Info,
        user_certificate_type: UserCertificateTypeInsertGQLModel,
        user_roles: typing.List[str],
        rbacobject_id: typing.Optional[IDType] = None
    ) -> typing.Union[UserCertificateTypeGQLModel, InsertError[UserCertificateTypeGQLModel]]:
        # Validate that startdate is before enddate if both are provided
        if user_certificate_type.startdate and user_certificate_type.enddate:
            if user_certificate_type.startdate >= user_certificate_type.enddate:
                return InsertError[UserCertificateTypeGQLModel](
                    msg="Start date must be before end date",
                    code="d5e8f9a2-4b3c-4d5e-9f8a-1b2c3d4e5f6a",
                    location="user_certificate_type_insert"
                )

        return await Insert[UserCertificateTypeGQLModel].DoItSafeWay(info=info, entity=user_certificate_type)
    

    @strawberry.mutation(
        description="""Update the UserCertificateType assignment""",
        permission_classes=[
            OnlyForAuthentized,
        ],
        extensions=[
            UserAccessControlExtension[UpdateError, UserCertificateTypeGQLModel](roles=["administrátor"]),
            UserRoleProviderExtension[UpdateError, UserCertificateTypeGQLModel](),
            RbacProviderExtension[UpdateError, UserCertificateTypeGQLModel](),
            LoadDataExtension[UpdateError, UserCertificateTypeGQLModel]()
        ],
    )
    async def user_certificate_type_update(
        self,
        info: strawberry.types.Info,
        user_certificate_type: UserCertificateTypeUpdateGQLModel,
        db_row: typing.Any,
        user_roles: typing.List[str],
        rbacobject_id: typing.Optional[IDType] = None
    ) -> typing.Union[UserCertificateTypeGQLModel, UpdateError[UserCertificateTypeGQLModel]]:
        # Validate dates if both are being updated
        startdate = user_certificate_type.startdate if user_certificate_type.startdate is not None else db_row.startdate
        enddate = user_certificate_type.enddate if user_certificate_type.enddate is not None else db_row.enddate

        if startdate and enddate and startdate >= enddate:
            return UpdateError[UserCertificateTypeGQLModel](
                _entity=db_row,
                msg="Start date must be before end date",
                code="e6f9a3b4-5c4d-5e6f-af9b-2c3d4e5f6a7b",
                location="user_certificate_type_update",
                _input=user_certificate_type
            )

        return await Update[UserCertificateTypeGQLModel].DoItSafeWay(info=info, entity=user_certificate_type)

    @strawberry.mutation(
        description="""Delete a UserCertificateType assignment""",
        permission_classes=[
            OnlyForAuthentized,
        ],
        extensions=[
            UserAccessControlExtension[DeleteError, UserCertificateTypeGQLModel](roles=["administrátor", "personalista"]),
            UserRoleProviderExtension[DeleteError, UserCertificateTypeGQLModel](),
            RbacProviderExtension[DeleteError, UserCertificateTypeGQLModel](),
            LoadDataExtension[DeleteError, UserCertificateTypeGQLModel]()
        ]
    )
    async def user_certificate_type_delete(
        self,
        info: strawberry.types.Info,
        user_certificate_type: UserCertificateTypeDeleteGQLModel,
        db_row: typing.Any,
        user_roles: typing.List[str],
        rbacobject_id: typing.Optional[IDType] = None
    ) -> typing.Optional[DeleteError[UserCertificateTypeGQLModel]]:
        return await Delete[UserCertificateTypeGQLModel].DoItSafeWay(info=info, entity=user_certificate_type)