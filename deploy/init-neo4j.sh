#!/bin/sh
set -eu

echo "Waiting for Neo4j..."
attempt=0
until cypher-shell \
  -a "${NEO4J_URI}" \
  -u "${NEO4J_USER}" \
  -p "${DB_PASSWORD}" \
  "RETURN 1;" >/dev/null 2>&1
do
  attempt=$((attempt + 1))
  if [ "${attempt}" -ge 60 ]; then
    echo "Neo4j did not become ready."
    exit 1
  fi
  sleep 2
done

for file in \
  /imports/schema.cypher \
  /imports/modules.cypher \
  /imports/knowledge-points.cypher \
  /imports/tools.cypher \
  /imports/media.cypher \
  /imports/relationships.cypher
do
  echo "Importing ${file}..."
  cypher-shell \
    -a "${NEO4J_URI}" \
    -u "${NEO4J_USER}" \
    -p "${DB_PASSWORD}" \
    --file "${file}"
done

echo "Neo4j initialization completed."
