# Copyright (c) 2026 ?????
# GIS???????????? - ????
# ?????????????????????

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


BACKEND_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = BACKEND_DIR.parent
SCRIPTS_DIR = ROOT_DIR / "scripts"

sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(SCRIPTS_DIR))

import main  # noqa: E402


@pytest.fixture(scope="session")
def client():
    with TestClient(main.app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def neo4j_client(client):
    response = client.get("/api/health")
    if response.status_code != 200:
        pytest.skip("Neo4j is not available for integration tests")
    return client
