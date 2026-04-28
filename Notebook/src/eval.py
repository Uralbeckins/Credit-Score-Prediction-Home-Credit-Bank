from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import brier_score_loss, roc_auc_score
import matplotlib.pyplot as plt

def get_score(pipeline, csv_name, X_Kaggle, X_validation, y_validation):

    # Сохраняем ID колонку из X_kaggle
    SK_ID_CURR = X_Kaggle['SK_ID_CURR'].copy()
    
    # Удаляем ID колонку для предсказания
    X_Kaggle_no_id = X_Kaggle.drop(columns=['SK_ID_CURR'])

    # Get predictions
    if pipeline.__name__ == 'SVC':
        y_kaggle_pred = pipeline.predict(X_Kaggle_no_id)
        y_val_pred = pipeline.predict(X_validation)

        


    else:
        y_kaggle_proba = pipeline.predict_proba(X_Kaggle_no_id)[:, 1]
        y_val_proba = pipeline.predict_proba(X_validation)[:, 1]

    # Make submission-file for Kaggle
    submission = pd.DataFrame({'SK_ID_CURR': SK_ID_CURR, 'TARGET': y_kaggle_proba})
    submission['SK_ID_CURR'] = submission['SK_ID_CURR'].astype(int)
    submission.to_csv(csv_name, index=False)

    # Plotting ROC-curve
    fpr, tpr, _ = roc_curve(y_validation,  y_val_proba)
    auc = roc_auc_score(y_validation, y_val_proba)

    plt.figure(figsize=(6, 6))
    plt.plot(fpr, tpr, label=f'AUC = {auc:.4f}', color='blue')
    plt.plot([0, 1], [0, 1], linestyle='--', color='green') # lame-classifier
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve')
    plt.legend(loc='lower right')
    plt.grid(True)
    plt.show()