

class CustomModel:

    def __init__(self, base_model):
        self.base_model = base_model

    def fit(self, X, y):
        self.base_model.fit(X, y)
        return self

    def predict(self, X):
        return self.base_model.predict_proba(X)[1,:]

    def get_model_params(self,):
       return self.__dict__


class CustomTransformer:

class CustomPreprocessor:

    def __init__(self, base_preprocessor):
