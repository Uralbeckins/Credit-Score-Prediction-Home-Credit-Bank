# 🐳 Инструкции по работе с Docker

Это руководство поможет вам собрать Docker образ и запушить его в Docker Hub.

## 📋 Предварительные требования

1. **Docker Desktop** установлен и запущен
2. **Аккаунт Docker Hub** (зарегистрируйтесь на [hub.docker.com](https://hub.docker.com))
3. **Терминал** (Terminal на macOS, PowerShell на Windows, или любой другой)

---

## 🏗️ Сборка Docker образа

### Вариант 1: Использование скрипта (рекомендуется)

```bash
# Из корня проекта
./docker/build.sh
```

Или с кастомным именем и тегом:
```bash
./docker/build.sh credit-score-prediction v1.0.0
```

### Вариант 2: Ручная сборка через Docker

```bash
# Из корня проекта
docker build -f docker/Dockerfile -t credit-score-prediction:latest .
```

---

## 🚀 Запуск контейнера

### Через Docker Desktop (GUI)

1. Откройте **Docker Desktop**
2. Перейдите в раздел **Images**
3. Найдите ваш образ `credit-score-prediction:latest`
4. Нажмите **Run**
5. В настройках укажите:
   - **Container name**: `credit-app` (или любое другое)
   - **Ports**: 
     - `8000:8000` (для FastAPI)
     - `8501:8501` (для Streamlit)
6. Нажмите **Run**

### Через командную строку

```bash
docker run -d \
  --name credit-app \
  -p 8000:8000 \
  -p 8501:8501 \
  credit-score-prediction:latest
```

После запуска:
- **FastAPI Backend**: http://localhost:8000/health
- **Streamlit Frontend**: http://localhost:8501

---

## 📤 Отправка образа в Docker Hub

### Шаг 1: Вход в Docker Hub

```bash
docker login
```

Введите ваш **username** и **password** от Docker Hub.

### Вариант 1: Использование скрипта (рекомендуется)

```bash
# Замените YOUR_USERNAME на ваше имя пользователя Docker Hub
./docker/push.sh YOUR_USERNAME
```

Или с кастомным именем и тегом:
```bash
./docker/push.sh YOUR_USERNAME credit-score-prediction v1.0.0
```

### Вариант 2: Комбинированный скрипт (сборка + пуш)

```bash
# Собирает образ и сразу пушит в Docker Hub
./docker/build-and-push.sh YOUR_USERNAME
```

### Вариант 3: Ручная отправка

```bash
# 1. Тегируем образ для Docker Hub
docker tag credit-score-prediction:latest YOUR_USERNAME/credit-score-prediction:latest

# 2. Пушим в Docker Hub
docker push YOUR_USERNAME/credit-score-prediction:latest
```

---

## 📥 Использование образа из Docker Hub

После того, как образ загружен в Docker Hub, вы можете использовать его на любом компьютере:

```bash
# Загрузка образа
docker pull YOUR_USERNAME/credit-score-prediction:latest

# Запуск контейнера
docker run -d \
  --name credit-app \
  -p 8000:8000 \
  -p 8501:8501 \
  YOUR_USERNAME/credit-score-prediction:latest
```

---

## 🔍 Полезные команды

### Просмотр запущенных контейнеров
```bash
docker ps
```

### Просмотр всех контейнеров (включая остановленные)
```bash
docker ps -a
```

### Остановка контейнера
```bash
docker stop credit-app
```

### Удаление контейнера
```bash
docker rm credit-app
```

### Просмотр логов контейнера
```bash
docker logs credit-app
```

### Просмотр логов в реальном времени
```bash
docker logs -f credit-app
```

### Просмотр образов
```bash
docker images
```

### Удаление образа
```bash
docker rmi credit-score-prediction:latest
```

---

## 🐛 Решение проблем

### Проблема: "Cannot connect to the Docker daemon"
**Решение**: Убедитесь, что Docker Desktop запущен.

### Проблема: "Permission denied" при выполнении скриптов
**Решение**: 
```bash
chmod +x docker/*.sh
```

### Проблема: Порты уже заняты
**Решение**: Измените порты в команде запуска:
```bash
docker run -d -p 8001:8000 -p 8502:8501 --name credit-app credit-score-prediction:latest
```

### Проблема: Образ не найден
**Решение**: Убедитесь, что вы собрали образ перед запуском:
```bash
./docker/build.sh
```

---

## 📝 Примеры использования

### Полный цикл: сборка → запуск → пуш

```bash
# 1. Сборка образа
./docker/build.sh myapp v1.0.0

# 2. Запуск контейнера
docker run -d --name credit-app -p 8000:8000 -p 8501:8501 myapp:v1.0.0

# 3. Проверка работы
curl http://localhost:8000/health
open http://localhost:8501

# 4. Остановка и удаление контейнера
docker stop credit-app
docker rm credit-app

# 5. Отправка в Docker Hub
./docker/push.sh YOUR_USERNAME myapp v1.0.0
```

---

## 🔗 Полезные ссылки

- [Docker Hub](https://hub.docker.com)
- [Docker Documentation](https://docs.docker.com)
- [Docker Desktop для macOS](https://docs.docker.com/desktop/install/mac-install/)

