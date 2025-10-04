# 🏦 Credit Score Prediction - Home Credit Bank

&#x20;

## О проекте

Это интерактивное приложение для оценки кредитного риска клиентов банка на основе данных соревнования Kaggle - [Home Credit Default Risk](https://www.kaggle.com/competitions/home-credit-default-risk)

Проект включает:

- **Jupyter Notebook**: полный pipeline с EDA, очисткой данных, feature engineering, обучением моделей и подбором гиперпараметров через Optuna.
- **FastAPI backend**: API для получения предсказаний модели.
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
└─ docs/
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

Проект использует широкий стек современных библиотек и инструментов для анализа данных, построения моделей машинного обучения, веб-приложений и деплоя:

### 1. Обработка и анализ данных

- **Pandas** — работа с табличными данными, очистка, агрегация и подготовка признаков.
- **NumPy** — эффективные численные вычисления и работа с массивами.
- **math, collections.Counter** — стандартные модули для математических операций и анализа распределений.

### 2. Визуализация данных

- **Matplotlib, Seaborn** — графики, histogram, boxplot, KDE для анализа распределений и выявления выбросов.
- **Heatmaps** — визуализация корреляций между признаками и таргетом.

### 3. Пропуски, масштабирование и кодирование признаков

- **sklearn.impute.SimpleImputer** — заполнение пропусков медианой или наиболее частым значением.
- **KNNImputer** — восстановление пропусков на основе ближайших соседей (опционально).
- **StandardScaler** — масштабирование (нормализация) числовых признаков.
- **OrdinalEncoder и OneHotEncoder** — кодирование категориальных признаков (порядковое и one-hot).
- **PolynomialFeatures** — генерация полиномиальных и производных признаков.

### 5. Machine Learning

- **Scikit-learn**:
  - LogisticRegression с пайплайном (масштабирование + регуляризация elasticnet)
  - DecisionTreeClassifier, RandomForestClassifier для обучения базовых и ансамблевых деревьев
  - Cross-validation и StratifiedKFold для надежной оценки моделей
  - ROC/AUC для метрик качества
- **CatBoost** — градиентный бустинг на деревьях, работающий с категориальными признаками без кодирования
- **Optuna** — автоматическая оптимизация гиперпараметров моделей
- **Joblib** — сохранение и загрузка обученных моделей и пайплайнов для последующего использования в API и веб-интерфейсе

### 6. Web-App и API

- **FastAPI** — быстрый backend API для получения предсказаний
- **Streamlit** — интерактивный веб-интерфейс

### 7. Контейнеризация и деплой

- **Docker** — изоляция приложений и зависимостей
- **Docker Compose** — запуск нескольких сервисов (backend + frontend)

---

## 📝 Модели и метрики

| Модель              | CV AUC | Kaggle Score |
| ------------------- | ------ | ------------ |
| Logistic Regression | 0.696  | 0.69638      |
| Decision Tree       | 0.540  | 0.53960      |
| Random Forest       | …      | …            |
| CatBoost            | …      | …            |


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

- Добавить автоматический сабмит на Kaggle
- Настроить деплой на сервер с HTTPS

---

## 📌 Лицензия

MIT License © Uralbeckins Corporation
All Rights Reserved

