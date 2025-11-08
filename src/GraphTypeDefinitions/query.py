import strawberry

from .EventGQLModel import EventQuery
from .EventInvitationGQLModel import EventInvitationQuery
from .RankGQLModel import RankGQLModel
from .UserGQLModel import UserGQLModel
from .UserRankGQLModel import UserRankGQLModel, UserRankQuery
from .RankGQLModel import RankQuery
from .CertificateTypeGQLModel import CertificateTypeQuery
from .CertificateCategoryGQLModel import CertificateCategoryQuery
from .WorkHistoryPositionGQLModel import WorkHistoryPositionQuery
from .StudyPlaceGQLModel import StudyPlaceQuery

@strawberry.type(description="""Type for query root""")
class Query(EventQuery, EventInvitationQuery, RankQuery, CertificateTypeQuery, UserRankQuery, CertificateCategoryQuery, WorkHistoryPositionQuery, StudyPlaceQuery):
    @strawberry.field(
        description="""Returns hello world"""
        )
    async def hello(
        self,
        info: strawberry.types.Info,
    ) -> str:
        return "hello world"
