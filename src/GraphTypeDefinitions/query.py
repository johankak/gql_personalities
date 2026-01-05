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
from .MedalCategoryGQLModel import MedalCategoryQuery
from .MedalTypeGQLModel import MedalTypeQuery
from .UserStudyPlaceGQLModel import UserStudyPlaceQuery
from .UserWorkHistoryPositionGQLModel import UserWorkHistoryPositionQuery

@strawberry.type(description="""Type for query root""")
class Query(EventQuery, EventInvitationQuery, RankQuery, CertificateTypeQuery, UserRankQuery, 
            WorkHistoryPositionQuery, StudyPlaceQuery, 
            MedalCategoryQuery, MedalTypeQuery, UserStudyPlaceQuery, UserWorkHistoryPositionQuery):
    @strawberry.field(
        description="""Returns hello world"""
        )
    async def hello(
        self,
        info: strawberry.types.Info,
    ) -> str:
        return "hello world"
