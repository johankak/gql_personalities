import strawberry

from .EventGQLModel import EventQuery
from .EventInvitationGQLModel import EventInvitationQuery
from .RanksGQLModel import RankGQLModel
from .UserGQLModel import UserGQLModel
from .UserRanksGQLModel import UserRankGQLModel, UserRanksQuery
from .RanksGQLModel import RankQuery
from .CertificateTypeGQLModel import CertificateTypeQuery


@strawberry.type(description="""Type for query root""")
class Query(EventQuery, EventInvitationQuery, RankQuery, CertificateTypeQuery, UserRanksQuery):
    @strawberry.field(
        description="""Returns hello world"""
        )
    async def hello(
        self,
        info: strawberry.types.Info,
    ) -> str:
        return "hello world"
