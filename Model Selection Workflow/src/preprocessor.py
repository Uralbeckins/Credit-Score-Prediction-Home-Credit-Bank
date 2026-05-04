from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder, PolynomialFeatures
from sklearn.base import BaseEstimator, TransformerMixin
from src import Config


class MyPreprocessor(BaseEstimator, TransformerMixin):
    def __init__(self, num_cols, cat_cols, ord_cols, ord_categories, n_neighbors=2):
        self.num_cols = num_cols
        self.cat_cols = cat_cols
        self.ord_cols = ord_cols
        self.ord_categories = ord_categories
        self.n_neighbors = n_neighbors
        
        num_branch = Pipeline([
            ('scaler', StandardScaler()),
            ('knn_imputer', SimpleImputer(strategy='median'))
        ])
        
        cat_branch = Pipeline([
            ('mode_imputer', SimpleImputer(strategy='most_frequent')),
            ('encoder', OneHotEncoder(drop='first', handle_unknown='ignore'))
        ])
        
        ord_branch = Pipeline([
            ('mode_imputer', SimpleImputer(strategy='most_frequent')),
            ('encoder', OrdinalEncoder(categories=ord_categories,
                                       handle_unknown='use_encoded_value',
                                       unknown_value=-1))
        ])

        # Combine all
        self.preprocessor_first = ColumnTransformer([
            ('numerical', num_branch, num_cols),
            ('categorical', cat_branch, cat_cols),
            ('ordinal', ord_branch, ord_cols)
        ], remainder='drop')

        # Separate columns for poly features (only those NOT in main preprocessor)
        poly_cols = [c for c in Config.POLY_FEATURES_COLS if c in (num_cols + cat_cols + ord_cols)]
        other_cols = [c for c in (num_cols + cat_cols + ord_cols) if c not in Config.POLY_FEATURES_COLS]

        if poly_cols:
            # Create separate preprocessor for poly_cols only
            preprocessor_for_poly = ColumnTransformer([
                ('numerical', num_branch, [c for c in poly_cols if c in num_cols]),
                ('categorical', cat_branch, [c for c in poly_cols if c in cat_cols]),
                ('ordinal', ord_branch, [c for c in poly_cols if c in ord_cols])
            ], remainder='drop')
            
            self.pipeline_poly = Pipeline([
                ('preprocessor', preprocessor_for_poly),
                ('poly_features', PolynomialFeatures(degree=Config.POLY_DEGREE,
                                                     include_bias=False,
                                                     interaction_only=False))
            ])

            # Create separate preprocessor for other_cols only
            preprocessor_for_other = ColumnTransformer([
                ('numerical', num_branch, [c for c in other_cols if c in num_cols]),
                ('categorical', cat_branch, [c for c in other_cols if c in cat_cols]),
                ('ordinal', ord_branch, [c for c in other_cols if c in ord_cols])
            ], remainder='drop')

            self.preprocessor = ColumnTransformer([
                ('main_pipeline', self.pipeline_poly, poly_cols),
                ('other_pipeline', preprocessor_for_other, other_cols)
            ], remainder='drop')
        else:
            self.preprocessor = self.preprocessor_first
    
    def fit(self, X, y=None):
        self.preprocessor.fit(X, y)
        return self
    
    def transform(self, X):
        return self.preprocessor.transform(X)
    
    def fit_transform(self, X, y=None):
        return self.preprocessor.fit_transform(X, y)