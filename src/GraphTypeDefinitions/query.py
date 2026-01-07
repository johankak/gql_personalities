import strawberry

from .EventGQLModel import EventQuery
from .EventInvitationGQLModel import EventInvitationQuery
from .RankGQLModel import RankGQLModel
from .UserGQLModel import UserGQLModel
from .UserRankGQLModel import UserRankGQLModel, UserRankQuery
from .RankGQLModel import RankQuery
from .CertificateTypeGQLModel import CertificateTypeQuery
from .WorkHistoryPositionGQLModel import WorkHistoryPositionQuery
from .StudyPlaceGQLModel import StudyPlaceQuery
from .MedalTypeGQLModel import MedalTypeQuery
from .UserStudyPlaceGQLModel import UserStudyPlaceQuery
from .UserWorkHistoryPositionGQLModel import UserWorkHistoryPositionQuery
from .UserCertificateTypeGQLModel import UserCertificateTypeQuery

@strawberry.type(description="""Type for query root""")
class Query(EventQuery, EventInvitationQuery, RankQuery, CertificateTypeQuery, UserRankQuery, 
            WorkHistoryPositionQuery, StudyPlaceQuery, 
            MedalTypeQuery, UserStudyPlaceQuery, UserWorkHistoryPositionQuery,
            UserCertificateTypeQuery):
    @strawberry.field(
        description="""Returns hello world"""
        )
    async def hello(
        self,
        info: strawberry.types.Info,
    ) -> str:
        return "hello world"
