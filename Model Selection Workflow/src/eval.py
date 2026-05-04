from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import brier_score_loss, roc_auc_score
from sklearn.model_selection import cross_val_score, StratifiedKFold
import matplotlib.pyplot as plt
from sklearn.calibration import calibration_curve
from src import Config


def get_stats(pipeline, X_train, y_train, X_val, y_val, cv_num=5):
    cv = StratifiedKFold(n_splits=cv_num, shuffle=True, random_state=Config.SEED)

    # ROC AUC через кросс-валидацию (среднее и std)
    auc_scores = cross_val_score(
        pipeline, X_val, y_val,
        cv=cv,
        scoring='roc_auc',
        n_jobs=-1,
        verbose=1
    )
    auc_mean = auc_scores.mean()
    auc_std = auc_scores.std()

    # Обучаем pipeline на всей валидационной выборке для proba и Brier score
    pipeline.fit(X_train, y_train)
    y_val_proba = pipeline.predict_proba(X_val)[:, 1]
    brier = brier_score_loss(y_val, y_val_proba)

    # Графики (опционально — можно убрать)
    _, axes = plt.subplots(1, 2, figsize=(12, 6))

    # ROC — показываем только легенду с auc_mean ± auc_std
    fpr, tpr, _ = roc_curve(y_val, y_val_proba)
    auc_plot = roc_auc_score(y_val, y_val_proba)

    axes[0].plot(fpr, tpr, label=f'AUC (plot) = {auc_plot:.4f}\nAUC (CV) = {auc_mean:.4f} ± {auc_std:.4f}', color='blue')
    axes[0].plot([0, 1], [0, 1], linestyle='--', color='green')
    axes[0].set_xlabel('False Positive Rate')
    axes[0].set_ylabel('True Positive Rate')
    axes[0].set_title('ROC Curve')
    axes[0].legend(loc='lower right')
    axes[0].grid(True)

    # Calibration curve
    prob_true_cal, prob_pred_cal = calibration_curve(y_val, y_val_proba, n_bins=15, strategy="uniform")
    axes[1].plot(prob_pred_cal, prob_true_cal, marker='o', linestyle='-', label=f'Brier = {brier:.4f}')
    axes[1].plot([0, 1], [0, 1], linestyle='--', color='gray', label='Perfectly Calibrated')
    axes[1].set_xlabel('Mean Predicted Probability')
    axes[1].set_ylabel('Fraction of Positives')
    axes[1].set_title('Calibration Curve')
    axes[1].legend()
    axes[1].grid(True)

    plt.show()

    return {
        'auc_mean_cv': round(auc_mean, 4),
        'auc_std_cv': round(auc_std, 4),
        'brier_score': round(brier, 4)
    }