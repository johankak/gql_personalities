import typing
import strawberry
from .BaseGQLModel import IDType


from uoishelpers.gqlpermissions import (
    OnlyForAuthentized
)
from uoishelpers.resolvers import (
    VectorResolver
)
from .EventInvitationGQLModel import EventInvitationGQLModel, EventInvitationInputFilter
from .RanksGQLModel import RankGQLModel
from .UserRanksGQLModel import UserRankGQLModel, UserRanksInputFilter

@strawberry.federation.type(extend=True, keys=["id"])
class UserGQLModel:
    id: IDType = strawberry.federation.field(external=True)

    from .BaseGQLModel import resolve_reference

    event_invitations: typing.List[EventInvitationGQLModel] = strawberry.field(
        description="Links to events where the user has been invited",
        permission_classes=[
            OnlyForAuthentized
        ],
        resolver=VectorResolver[EventInvitationGQLModel](fkey_field_name="user_id", whereType=EventInvitationInputFilter)
    )

    # @strawberry.field(description="Ranks assigned to the user", permission_classes=[OnlyForAuthentized])
    # async def ranks(self, info:strawberry.types.Info) -> typing.List["RankGQLModel"]:
    #     return []
    #     from uoishelpers.dbsession import get_db_session_from_info
    #     from src.DBDefinitions.UserRanksModel import UserRanksModel
    #     session = get_db_session_from_info(info)
    #     user_ranks = await session.execute(
    #         sqlalchemy.select(UserRanksModel).where(UserRanksModel.user_id == self.id)
    #     )
    #     user_ranks_instances = user_ranks.scalars().all()
    #     rank_ids = [ur.rank_id for ur in user_ranks_instances if ur.rank_id is not None]
    #     if not rank_ids:
    #         return []
    #     ranks = await session.execute(
    #         sqlalchemy.select(RankGQLModel._meta.model).where(RankGQLModel._meta.model.id.in_(rank_ids))
    #     )
    #     rank_instances = ranks.scalars().all()
    #     return [RankGQLModel.from_instance(rank) for rank in rank_instances]
    
    ranks: typing.List[UserRankGQLModel] = strawberry.field(
        description="Links to events where the user has been invited",
        permission_classes=[
            OnlyForAuthentized
        ],
        
        resolver=VectorResolver[UserRankGQLModel](fkey_field_name="user_id", whereType=UserRanksInputFilter)
    )
    # async def event_invitations(self, info:strawberry.types.Info)