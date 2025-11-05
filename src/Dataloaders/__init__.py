# from uoishelpers.dataloaders import createIdLoader, createFkeyLoader
# from functools import cache

from src.DBDefinitions import BaseModel
from src.DBDefinitions import (
    EventModel,
    EventInvitationModel,
    UserRankModel,
    RankModel,
    CertificateTypeModel,
    CertificateCategoryModel

)

from uoishelpers.dataloaders.LoaderMapBase import LoaderMapBase
from uoishelpers.dataloaders.IDLoader import IDLoader
import src.DBDefinitions

class LoaderMap(LoaderMapBase[BaseModel]):
    """LoaderMap is a map of IDLoaders for all models in the BaseModel registry.
    It is used to create loaders for all models in the BaseModel registry.
    """
    BaseModel = BaseModel

    EventModel: IDLoader[src.DBDefinitions.EventModel] = None
    EventInvitationModel: IDLoader[src.DBDefinitions.EventInvitationModel] = None
    RankModel: IDLoader[src.DBDefinitions.RankModel] = None
    CertificateTypeModel: IDLoader[src.DBDefinitions.CertificateTypeModel] = None
    UserRanksModel: IDLoader[src.DBDefinitions.UserRankModel] = None
    CertificateCategoryModel: IDLoader[src.DBDefinitions.CertificateCategoryModel] = None


    def __init__(self, session):
        super().__init__(session)

        self.EventModel = self.get(EventModel)
        self.EventInvitationModel = self.get(EventInvitationModel)
        self.RankModel = self.get(RankModel)
        self.CertificateTypeModel = self.get(CertificateTypeModel)
        self.UserRanksModel = self.get(UserRankModel)
        self.CertificateCategoryModel = self.get(CertificateCategoryModel)


        # print(f"LoaderMap created with session: {session}")

def createLoadersContext(session):
    return {
        "loaders": LoaderMap(session)
    }
