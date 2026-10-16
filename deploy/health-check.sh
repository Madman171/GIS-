#!/bin/sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/.env"
COMPOSE_FILE="${SCRIPT_DIR}/docker-compose.yml"

PUBLIC_PORT="$(grep '^PUBLIC_PORT=' "${ENV_FILE}" \
  | tail -n 1 \
  | cut -d '=' -f 2- \
  | tr -d '\r')"
PUBLIC_PORT="${PUBLIC_PORT:-8080}"

docker compose \
  --env-file "${ENV_FILE}" \
  -f "${COMPOSE_FILE}" \
  ps

echo "Checking frontend..."
curl -fsS "http://127.0.0.1:${PUBLIC_PORT}/" >/dev/null

echo "Checking backend..."
curl -fsS "http://127.0.0.1:${PUBLIC_PORT}/api/health"

echo
echo "Health check passed."
