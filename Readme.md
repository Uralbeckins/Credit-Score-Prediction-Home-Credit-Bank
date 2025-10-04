# 🏦 Credit Score Prediction - Home Credit Bank

&#x20;
<p align="center">
  <img src="https://img.shields.io/badge/Optuna-0090FF?logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/CatBoost-FFCC00?logo=catboost&logoColor=black" alt="Python Version">
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?logo=scikitlearn&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white" alt="Jupyter">
  <img src="https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white" alt="Model">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
</p>

---

## 🧠 О проекте

**Credit Score Prediction** — это проект по предсказанию кредитоспособности клиентов банка **Home Credit**, основанный на реальных данных с Kaggle - [Home Credit Default Risk](https://www.kaggle.com/competitions/home-credit-default-risk)

Цель — определить вероятность того, что клиент не сможет вовремя вернуть кредит, используя данные о доходах, работе, семье и кредитной истории.

---

## 🖼 Скриншоты интерфейса
<img width="583" height="319" alt="image" src="https://github.com/user-attachments/assets/6b101392-0477-4fa2-8a79-a78d13308075" />
<img width="599" height="225" alt="image" src="https://github.com/user-attachments/assets/382b9cb9-8ab3-4116-b5fd-0dcac95edf47" />
<img width="582" height="186" alt="image" src="https://github.com/user-attachments/assets/0ca0c6d4-0649-4dcc-b82c-bf77f308db93" />

---

### Проект включает:

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
## 🧩 Используемые технологии

Проект использует широкий стек современных библиотек и инструментов для анализа данных, построения моделей машинного обучения, веб-приложений и деплоя:

### 1. 📊 Обработка и анализ данных

- **Pandas** — работа с табличными данными, очистка, агрегация и подготовка признаков.
- **NumPy** — эффективные численные вычисления и работа с массивами.
- **math, collections.Counter** — стандартные модули для математических операций и анализа распределений.

### 2. 📈 Визуализация данных

- **Matplotlib, Seaborn** — графики, histogram, boxplot, KDE для анализа распределений и выявления выбросов.
- **Heatmaps** — визуализация корреляций между признаками и таргетом.

### 3. 🧩 Пропуски, масштабирование и кодирование признаков

- **sklearn.impute.SimpleImputer** — заполнение пропусков медианой или наиболее частым значением.
- **KNNImputer** — восстановление пропусков на основе ближайших соседей (опционально).
- **StandardScaler** — масштабирование (нормализация) числовых признаков.
- **OrdinalEncoder и OneHotEncoder** — кодирование категориальных признаков (порядковое и one-hot).
- **PolynomialFeatures** — генерация полиномиальных и производных признаков.

### 5. 🧠 Machine Learning

- **Scikit-learn**:
  - LogisticRegression с пайплайном (масштабирование + регуляризация elasticnet)
  - DecisionTreeClassifier, RandomForestClassifier для обучения базовых и ансамблевых деревьев
  - Cross-validation и StratifiedKFold для надежной оценки моделей
  - ROC/AUC для метрик качества
- **CatBoost** — градиентный бустинг на деревьях, работающий с категориальными признаками без кодирования
- **Optuna** — автоматическая оптимизация гиперпараметров моделей
- **Joblib** — сохранение и загрузка обученных моделей и пайплайнов для последующего использования в API и веб-интерфейсе

### 6. 🛜 Web-App и API

- **FastAPI** — быстрый backend API для получения предсказаний
- **Streamlit** — интерактивный веб-интерфейс

### 7. 💻 Контейнеризация и деплой

- **Docker** — изоляция приложений и зависимостей
- **Docker Compose** — запуск нескольких сервисов (backend + frontend)

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

## 📝 Модели и метрики

| Модель              | CV AUC | Kaggle Score |
| ------------------- | ------ | ------------ |
| Logistic Regression | 0.696  | 0.69638      |
| Decision Tree       | 0.540  | 0.53960      |
| Random Forest       | …      | …            |
| CatBoost            | …      | …            |


## 💾 Сохраненные модели

- `pipeline_logreg.joblib` — **Логистическая регрессия** с пайплайном (`StandardScaler` + `LogisticRegression`).  
  Простая и интерпретируемая модель, использовалась как базовая для сравнения.

- `best_model_catboost` — **CatBoostClassifier** от Яндекса.  
  Отлично справился с категориальными признаками без необходимости ручного кодирования, показал высокую точность.

- `best_model_xgboost` — **XGBoostClassifier**.  
  Градиентный бустинг на деревьях решений, продемонстрировал хорошее качество и устойчивость к переобучению.

- `best_model_random_forest` — **RandomForestClassifier**.  
  Ансамблевая модель из множества деревьев решений, обеспечила стабильные результаты и хорошую интерпретируемость признаков.

- `best_model_decision_tree` — **DecisionTreeClassifier**.  
  Простая модель дерева решений, использовалась для анализа важности признаков и визуализации процесса классификации.

---

## 🔧 Дальнейшие шаги

- Добавить автоматический сабмит на Kaggle
- Настроить деплой на сервер с HTTPS

---

## 📌 Лицензия

MIT License © Uralbeckins Corporation
All Rights Reserved

