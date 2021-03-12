from StudentPerformancePrediction import models


# region Aagam Sheth
class PredictionDataRouter(object):
    def db_for_read(self, model, **hints):
        if model == models.PredictionData:
            return 'pred'

    def db_for_write(self, model, **hints):
        if model == models.PredictionData:
            return 'pred'

    def allow_relation(self, obj1, obj2, **hints):
        if (
                obj1._meta.app_label == "StudentPerformancePrediction" or
                obj2._meta.app_label == "StudentPerformancePrediction"
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name == "predictiondata":
            return db == 'pred'
        return None
# endregion
