# from uoishelpers.dataloaders import createIdLoader, createFkeyLoader
# from functools import cache

from src.DBDefinitions import BaseModel
from src.DBDefinitions import (
    EventModel,
    EventInvitationModel,
    UserRankModel,
    RankModel,
    CertificateTypeModel,
    CertificateCategoryModel,
    WorkHistoryPositionModel,
    StudyPlaceModel,
    MedalCategoryModel,
    MedalTypeModel

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
    UserRankModel: IDLoader[src.DBDefinitions.UserRankModel] = None
    CertificateCategoryModel: IDLoader[src.DBDefinitions.CertificateCategoryModel] = None
    WorkHistoryPositionModel: IDLoader[src.DBDefinitions.WorkHistoryPositionModel] = None
    StudyPlaceModel: IDLoader[src.DBDefinitions.StudyPlaceModel] = None 
    MedalCategoryModel: IDLoader[src.DBDefinitions.MedalCategoryModel] = None
    MedalTypeModel: IDLoader[src.DBDefinitions.MedalTypeModel] = None

    def __init__(self, session):
        super().__init__(session)

        self.EventModel = self.get(EventModel)
        self.EventInvitationModel = self.get(EventInvitationModel)
        self.RankModel = self.get(RankModel)
        self.CertificateTypeModel = self.get(CertificateTypeModel)
        self.UserRankModel = self.get(UserRankModel)
        self.CertificateCategoryModel = self.get(CertificateCategoryModel)
        self.WorkHistoryPositionModel = self.get(WorkHistoryPositionModel)
        self.StudyPlaceModel = self.get(StudyPlaceModel)
        self.MedalCategoryModel = self.get(MedalCategoryModel)
        self.MedalTypeModel = self.get(MedalTypeModel)
        # print(f"LoaderMap created with session: {session}")

def createLoadersContext(session):
    return {
        "loaders": LoaderMap(session)
    }
