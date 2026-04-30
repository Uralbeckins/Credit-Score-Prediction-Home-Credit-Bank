from src import Config
import pandas as pd

def get_num_cat_ord_cols(df: pd.DataFrame):
    """
    Возвращает списки numeric, categorical и ordinal колонок на основе DataFrame и Config
    """
    df = df.copy()
    
    # Удаляем целевую колонку, если она есть
    if Config.TARGET_COL and Config.TARGET_COL in df.columns:
        df.drop(columns=[Config.TARGET_COL], inplace=True)
    
    # Удаляем колонки из DROP_COLS, если они существуют
    if Config.DROP_COLS:
        existing_drop_cols = [col for col in Config.DROP_COLS if col in df.columns]
        df.drop(columns=existing_drop_cols, inplace=True)
    
    all_columns = set(df.columns)
    
    ord_cols = {col for col in Config.ORDINAL_COLS if col in all_columns}
    num_cols = set(df.select_dtypes(include=['int64', 'float64', 'bool']).columns) - ord_cols
    cat_cols = set(df.select_dtypes(include=['object', 'category']).columns) - ord_cols

    ordinal_categories = _generate_ordinal_categories(df, list(ord_cols))
    
    return sorted(num_cols), sorted(cat_cols), sorted(ord_cols), ordinal_categories


def prepare_data(df: pd.DataFrame):
    """
    Подготавливает DataFrame, удаляя целевую колонку и колонки из DROP_COLS
    """
    df = df.copy()
    
    if Config.TARGET_COL in df.columns:
        target = df[Config.TARGET_COL]
        df.drop(columns=[Config.TARGET_COL], inplace=True)
    else:
        raise ValueError(f"Целевая переменная '{Config.TARGET_COL}' отсутствует в DataFrame.")
    
    if Config.DROP_COLS and any(col in df.columns for col in Config.DROP_COLS):
        existing_drop_cols = [col for col in Config.DROP_COLS if col in df.columns]
        df.drop(columns=existing_drop_cols, inplace=True)

    
    
    return df, target


def _generate_ordinal_categories(df: pd.DataFrame, ord_cols: list):
    """Генерирует список категорий для OrdinalEncoder"""
    categories = []
    
    # Категории для NAME_EDUCATION_TYPE с фиксированным порядком
    education_categories = [
        'Lower secondary',
        'Secondary / secondary special', 
        'Incomplete higher',
        'Higher education',
        'Academic degree'
    ]
    categories.append(education_categories)
    
    # Для остальных колонок - уникальные значения в порядке появления (без NaN)
    for col in ord_cols:
        if 'NAME_EDUCATION_TYPE' in col:
            continue
        # Убираем NaN значения из уникальных категорий
        cats = [cat for cat in df[col].unique() if pd.notna(cat)]
        categories.append(cats)
    
    return categories