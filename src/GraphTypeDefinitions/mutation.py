import strawberry


from .EventGQLModel import EventMutation
from .EventInvitationGQLModel import EventInvitationMutation
from .MedalTypeGQLModel import MedalTypeMutation
from .MedalCategoryGQLModel import MedalCategoryMutation
from .RankGQLModel import RankMutation
from .CertificateCategoryGQLModel import CertificateCategoryMutation
from .CertificateTypeGQLModel import CertificateTypeMutation
from .WorkHistoryPositionGQLModel import WorkHistoryPositionMutation
from .StudyPlaceGQLModel import StudyPlaceMutation

@strawberry.type(description="""Type for mutation root""")
class Mutation(EventMutation, EventInvitationMutation, MedalTypeMutation, RankMutation, CertificateCategoryMutation,
               CertificateTypeMutation, MedalCategoryMutation, WorkHistoryPositionMutation, StudyPlaceMutation):
    pass

