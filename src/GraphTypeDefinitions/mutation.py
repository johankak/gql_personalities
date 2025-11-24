import strawberry


from .EventGQLModel import EventMutation
from .EventInvitationGQLModel import EventInvitationMutation
from .MedalTypeGQLModel import MedalTypeMutation

@strawberry.type(description="""Type for mutation root""")
class Mutation(EventMutation, EventInvitationMutation, MedalTypeMutation):
    pass

