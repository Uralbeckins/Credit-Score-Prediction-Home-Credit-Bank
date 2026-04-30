from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.base import BaseEstimator, TransformerMixin


class MyPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self, num_cols, cat_cols, ord_cols, ord_categories, n_neighbors=2):
        self.num_cols = num_cols
        self.cat_cols = cat_cols
        self.ord_cols = ord_cols
        self.ord_categories = ord_categories
        self.n_neighbors = n_neighbors
        
        # Numerical branch: scale -> KNN impute
        num_branch = Pipeline([
            ('scaler', StandardScaler()),
            ('knn_imputer', KNNImputer(n_neighbors=n_neighbors))
        ])
        
        # Categorical branch: mode impute (KNN doesn't work well for categorical)
        cat_branch = Pipeline([
            ('mode_imputer', SimpleImputer(strategy='most_frequent')),
            ('encoder', OneHotEncoder(drop='first', handle_unknown='ignore'))
        ])
        
        # Ordinal branch: mode impute -> ordinal encode
        ord_branch = Pipeline([
            ('mode_imputer', SimpleImputer(strategy='most_frequent')),
            ('encoder', OrdinalEncoder(categories=ord_categories,
                                       handle_unknown='use_encoded_value',
                                       unknown_value=-1))
        ])
        
        # Combine all
        self.preprocessor = ColumnTransformer([
            ('numerical', num_branch, num_cols),
            ('categorical', cat_branch, cat_cols),
            ('ordinal', ord_branch, ord_cols)
        ], remainder='drop')
    
    def fit(self, X, y=None):
        self.preprocessor.fit(X, y)
        return self
    
    def transform(self, X):
        return self.preprocessor.transform(X)
    
    def fit_transform(self, X, y=None):
        return self.preprocessor.fit_transform(X, y)