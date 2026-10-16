#!/bin/sh
set -eu

if [ "$(id -u)" -eq 0 ]; then
  SUDO=""
else
  SUDO="sudo"
fi

${SUDO} apt-get update
${SUDO} apt-get install -y ca-certificates curl
curl -fsSL https://get.docker.com | ${SUDO} sh

if [ -n "${SUDO}" ]; then
  ${SUDO} usermod -aG docker "${USER}"
  echo "Docker installed. Log out and log in again before running deploy.sh."
else
  echo "Docker installed."
fi

