#!/bin/sh
# Optional startup script — currently not required because supervisord launches both services.
# Kept for future init steps (migrations, permission fixes, etc.).
set -e

echo "Starting container initialization..."
# Example: wait for model file or prepare environment here
if [ -n "${MODEL_PATH}" ] && [ ! -f "${MODEL_PATH}" ]; then
  echo "Warning: MODEL_PATH is set but file not found: ${MODEL_PATH}"
fi

echo "Initialization complete."
exec "$@"
