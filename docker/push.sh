#!/bin/bash

# Скрипт для пуша Docker образа в Docker Hub
# Использование: ./docker/push.sh [dockerhub_username] [имя_образа] [тег]

set -e

# Получаем путь к корню проекта
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Параметры
DOCKERHUB_USERNAME="${1}"
IMAGE_NAME="${2:-credit-score-prediction}"
TAG="${3:-latest}"

if [ -z "$DOCKERHUB_USERNAME" ]; then
    echo "❌ Ошибка: необходимо указать имя пользователя Docker Hub"
    echo ""
    echo "Использование: ./docker/push.sh <dockerhub_username> [имя_образа] [тег]"
    echo ""
    echo "Пример: ./docker/push.sh myusername"
    echo "Пример: ./docker/push.sh myusername credit-score-prediction v1.0.0"
    exit 1
fi

FULL_IMAGE_NAME="${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${TAG}"
LOCAL_IMAGE_NAME="${IMAGE_NAME}:${TAG}"

echo "🔍 Проверка наличия локального образа..."
if ! docker image inspect "$LOCAL_IMAGE_NAME" &> /dev/null; then
    echo "⚠️  Локальный образ $LOCAL_IMAGE_NAME не найден"
    echo "📦 Сначала соберите образ с помощью: ./docker/build.sh $IMAGE_NAME $TAG"
    exit 1
fi

echo "🏷️  Тегирование образа для Docker Hub..."
docker tag "$LOCAL_IMAGE_NAME" "$FULL_IMAGE_NAME"

echo ""
echo "🔐 Вход в Docker Hub..."
echo "   (Введите ваш пароль Docker Hub при запросе)"
docker login

echo ""
echo "📤 Отправка образа в Docker Hub..."
docker push "$FULL_IMAGE_NAME"

echo ""
echo "✅ Образ успешно отправлен в Docker Hub!"
echo "🔗 URL образа: https://hub.docker.com/r/$DOCKERHUB_USERNAME/$IMAGE_NAME"
echo ""
echo "📥 Для загрузки образа на другом компьютере используйте:"
echo "   docker pull $FULL_IMAGE_NAME"
echo ""
echo "🚀 Для запуска образа используйте:"
echo "   docker run -d -p 8000:8000 -p 8501:8501 --name credit-app $FULL_IMAGE_NAME"

