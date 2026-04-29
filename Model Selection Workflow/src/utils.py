from src import Config
import pandas as pd

def get_num_cat_ord_cols(df: pd.DataFrame, ord_cols: list = Config.ORDINAL_COLS, target_col: str = Config.TARGET_COL):
    
    if target_col in df.columns:
        df.drop(columns=[target_col], inplace=True)

    num_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    # добавить вычитание для ord_cols
    ord_cols = ord_cols if ord_cols is not None else []

    return num_cols, cat_cols, ord_cols