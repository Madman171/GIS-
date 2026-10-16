#!/bin/sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/.env"
COMPOSE_FILE="${SCRIPT_DIR}/docker-compose.yml"
BACKUP_DIR="${SCRIPT_DIR}/backups"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"

mkdir -p "${BACKUP_DIR}"

docker compose \
  --env-file "${ENV_FILE}" \
  -f "${COMPOSE_FILE}" \
  stop neo4j

docker run --rm \
  -v gis-knowledge-platform_neo4j_data:/data:ro \
  -v "${BACKUP_DIR}:/backup" \
  alpine:3.22 \
  tar -czf "/backup/neo4j-data-${TIMESTAMP}.tar.gz" -C /data .

docker compose \
  --env-file "${ENV_FILE}" \
  -f "${COMPOSE_FILE}" \
  start neo4j

tar -czf \
  "${BACKUP_DIR}/media-${TIMESTAMP}.tar.gz" \
  -C "${SCRIPT_DIR}/../backend" \
  media

echo "Backup completed: ${BACKUP_DIR}"

