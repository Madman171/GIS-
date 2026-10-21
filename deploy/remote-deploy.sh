#!/bin/sh
set -eu

DEPLOY_PATH="${DEPLOY_PATH:-/opt/gis-knowledge-platform}"
TARGET_TAG="${1:?Usage: remote-deploy.sh <release-tag>}"

cd "$DEPLOY_PATH"
git fetch --prune origin main --tags
TARGET_SHA="$(git rev-parse "${TARGET_TAG}^{commit}")"
PREVIOUS_SHA="$(git rev-parse HEAD)"

deploy_current() {
  sh deploy/deploy.sh
  sh deploy/health-check.sh
}

git checkout --detach "$TARGET_SHA"
if deploy_current; then
  echo "Deployment succeeded: ${TARGET_TAG} (${TARGET_SHA})"
  exit 0
fi

echo "Deployment failed; rolling back to ${PREVIOUS_SHA}" >&2
git checkout --detach "$PREVIOUS_SHA"
deploy_current
exit 1
