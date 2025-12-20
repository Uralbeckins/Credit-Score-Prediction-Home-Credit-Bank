#!/bin/bash

# Скрипт для сборки Docker образа
# Использование: ./docker/build.sh [имя_образа] [тег]

set -e

# Получаем путь к корню проекта
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Параметры по умолчанию
IMAGE_NAME="${1:-credit-score-prediction}"
TAG="${2:-latest}"
FULL_IMAGE_NAME="${IMAGE_NAME}:${TAG}"

echo "🏗️  Сборка Docker образа..."
echo "📦 Имя образа: $FULL_IMAGE_NAME"
echo "📁 Контекст сборки: $PROJECT_ROOT"
echo ""

# Сборка образа
docker build \
    -f docker/Dockerfile \
    -t "$FULL_IMAGE_NAME" \
    "$PROJECT_ROOT"

echo ""
echo "✅ Образ успешно собран: $FULL_IMAGE_NAME"
echo ""
echo "🚀 Для запуска контейнера используйте:"
echo "   docker run -d -p 8000:8000 -p 8501:8501 --name credit-app $FULL_IMAGE_NAME"
echo ""
echo "📝 Или используйте Docker Desktop для запуска через GUI"

