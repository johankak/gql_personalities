import strawberry


from .EventGQLModel import EventMutation
from .EventInvitationGQLModel import EventInvitationMutation
from .MedalTypeGQLModel import MedalTypeMutation
from .RankGQLModel import RankMutation
from .CertificateTypeGQLModel import CertificateTypeMutation
from .WorkHistoryPositionGQLModel import WorkHistoryPositionMutation
from .StudyPlaceGQLModel import StudyPlaceMutation
from .UserRankGQLModel import UserRankMutation
from .UserStudyPlaceGQLModel import UserStudyPlaceMutation
from .UserWorkHistoryPositionGQLModel import UserWorkHistoryPositionMutation
from .UserCertificateTypeGQLModel import UserCertificateTypeMutation
from .UserMedalTypeGQLModel import UserMedalTypeMutation

@strawberry.type(description="""Type for mutation root""")
class Mutation(EventMutation, EventInvitationMutation, MedalTypeMutation, RankMutation, 
               CertificateTypeMutation, 
               WorkHistoryPositionMutation, StudyPlaceMutation, UserRankMutation, UserStudyPlaceMutation,
               UserWorkHistoryPositionMutation, UserCertificateTypeMutation, UserMedalTypeMutation):
    pass

