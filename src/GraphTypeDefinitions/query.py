import strawberry

from .EventGQLModel import EventQuery
from .EventInvitationGQLModel import EventInvitationQuery
from .RanksGQLModel import RankGQLModel
from .UserGQLModel import UserGQLModel
from .UserRanksGQLModel import UserRanksGQLModel
from .RanksGQLModel import RankQuery
@strawberry.type(description="""Type for query root""")
class Query(EventQuery, EventInvitationQuery, RankQuery):
    @strawberry.field(
        description="""Returns hello world"""
        )
    async def hello(
        self,
        info: strawberry.types.Info,
    ) -> str:
        return "hello world"
