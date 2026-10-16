#!/bin/sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/.env"
COMPOSE_FILE="${SCRIPT_DIR}/docker-compose.yml"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is not installed. Run deploy/install-docker-ubuntu.sh first."
  exit 1
fi

if [ ! -f "${ENV_FILE}" ]; then
  cp "${SCRIPT_DIR}/.env.production.example" "${ENV_FILE}"
  echo "Created ${ENV_FILE}. Fill in the secrets and run this script again."
  exit 1
fi

if grep -q "请替换" "${ENV_FILE}"; then
  echo "Please replace placeholder values in ${ENV_FILE}."
  exit 1
fi

docker compose \
  --env-file "${ENV_FILE}" \
  -f "${COMPOSE_FILE}" \
  build

docker compose \
  --env-file "${ENV_FILE}" \
  -f "${COMPOSE_FILE}" \
  up -d

echo "Services started. Waiting for the backend..."
sleep 15

sh "${SCRIPT_DIR}/health-check.sh"

