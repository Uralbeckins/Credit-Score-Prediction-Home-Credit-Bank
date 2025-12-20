#!/bin/bash

# Комбинированный скрипт для сборки и пуша образа в Docker Hub
# Использование: ./docker/build-and-push.sh [dockerhub_username] [имя_образа] [тег]

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
    echo "Использование: ./docker/build-and-push.sh <dockerhub_username> [имя_образа] [тег]"
    echo ""
    echo "Пример: ./docker/build-and-push.sh myusername"
    echo "Пример: ./docker/build-and-push.sh myusername credit-score-prediction v1.0.0"
    exit 1
fi

echo "🚀 Начинаем процесс сборки и отправки образа..."
echo ""

# Шаг 1: Сборка
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 ШАГ 1: Сборка образа"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
"$PROJECT_ROOT/docker/build.sh" "$IMAGE_NAME" "$TAG"

# Шаг 2: Пуш
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📤 ШАГ 2: Отправка в Docker Hub"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
"$PROJECT_ROOT/docker/push.sh" "$DOCKERHUB_USERNAME" "$IMAGE_NAME" "$TAG"

echo ""
echo "🎉 Готово! Образ собран и отправлен в Docker Hub"

