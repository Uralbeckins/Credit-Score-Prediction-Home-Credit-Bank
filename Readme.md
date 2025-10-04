# 🏦 Credit Score Prediction - Home Credit Bank

&#x20;

## О проекте

Это интерактивное приложение для оценки кредитного риска клиентов банка на основе данных соревнования [Home Credit Default Risk](https://www.kaggle.com/competitions/home-credit-default-risk).

Проект включает:

- **Jupyter Notebook**: полный pipeline с EDA, очисткой данных, feature engineering, обучением моделей и подбором гиперпараметров через Optuna.
- **FastAPI backend**: REST API для получения предсказаний модели.
- **Streamlit frontend**: веб-интерфейс для интерактивного тестирования кредитного скоринга.
- **Docker**: контейнеризация для простого запуска и деплоя.

---

## 🗂 Структура проекта

```
Credit-Score-Prediction-Home-Credit-Bank/
│
├─ notebook.ipynb               # Jupyter Notebook с обработкой данных и моделями
├─ backend/
│   ├─ main.py                  # FastAPI backend
│   ├─ models/                  # сохраненные модели (pipeline_logreg.joblib и др.)
│   └─ requirements.txt
├─ web/
│   ├─ app.py                   # Streamlit frontend
│   └─ requirements.txt
├─ docker-compose.yml
├─ README.md
└─ docs/                        # скриншоты интерфейса, баннеры
```

---

## ⚡ Быстрый старт (локально)

### 1. Клонируем репозиторий

```bash
git clone https://github.com/Uralbeckins/Credit-Score-Prediction-Home-Credit-Bank.git
cd Credit-Score-Prediction-Home-Credit-Bank
```

### 2. Собираем и запускаем контейнеры

```bash
docker-compose up --build
```

- **FastAPI backend**: `http://localhost:8000/health`
- **Streamlit frontend**: `http://localhost:8501`

---

## 🧩 Используемые технологии

- **Python 3.9**
- **Pandas, NumPy, Scikit-learn, CatBoost** — обработка данных и обучение моделей
- **Optuna** — подбор гиперпараметров
- **FastAPI** — backend API
- **Streamlit** — интерактивный веб-интерфейс
- **Docker & Docker Compose** — контейнеризация и локальный деплой

---

## 📝 Модели и метрики

| Модель              | CV AUC | Kaggle Score |
| ------------------- | ------ | ------------ |
| Logistic Regression | 0.696  | 0.69638      |
| Decision Tree       | 0.540  | 0.53960      |
| Random Forest       | …      | …            |
| CatBoost            | …      | …            |

> Для повышения точности применены полиномиальные признаки и feature engineering.

---

## 🖼 Скриншоты интерфейса

\


> Замените эти картинки на свои скриншоты из веб-интерфейса.

---

## 💾 Сохраненные модели

- `pipeline_logreg.joblib` — логистическая регрессия с пайплайном (StandardScaler + LogisticRegression)
- Другие модели можно добавить после обучения через Optuna.

---

## 🔧 Дальнейшие шаги

- Оптимизировать CatBoost / RandomForest для больших данных
- Добавить автоматический сабмит на Kaggle
- Настроить деплой в облаке с HTTPS
- Добавить аутентификацию и rate-limiting для FastAPI

---

## 📌 Лицензия

MIT License © Uralbeckins

