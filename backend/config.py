# Copyright (c) 2026 ?????
# GIS???????????? - ????
# ?????????????????????

# Copyright (c) 2026 版权所有人
# GIS交通路网教学知识图谱平台 - 后端服务
# 本文件为平台核心业务代码，受软件著作权保护

import os
from pathlib import Path
from typing import List

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


if load_dotenv:
    load_dotenv(Path(__file__).with_name(".env"))


def _string_list(name: str, default: str) -> List[str]:
    raw_value = os.getenv(name, default)
    return [item.strip() for item in raw_value.split(",") if item.strip()]


def _get_origins() -> List[str]:
    return _string_list(
        "CORS_ALLOW_ORIGINS",
        (
            "http://localhost:9080,http://127.0.0.1:9080,"
            "http://localhost:5173,http://127.0.0.1:5173"
        ),
    )


# GIS交通路网教学知识图谱平台专属数据库配置。
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "traffic_kg")

# 教学知识图谱业务配置。
KG_CONFIG = {
    "max_learning_path_length": int(
        os.getenv("KG_MAX_LEARNING_PATH_LENGTH", "8")
    ),
    "enable_topology_check": os.getenv(
        "ENABLE_TOPOLOGY_CHECK",
        "true",
    ).strip().lower()
    in {"1", "true", "yes", "on"},
    "coordinate_tolerance": float(
        os.getenv("TOPOLOGY_COORDINATE_TOLERANCE", "1.0")
    ),
}

# GIS交通路网教学问答引擎专属配置。
QA_CONFIG = {
    "max_references": int(os.getenv("ANSWER_MAX_REFERENCES", "6")),
    "rate_limit_per_minute": int(
        os.getenv("CHAT_RATE_LIMIT_PER_MINUTE", "5")
    ),
    "whitelist": _string_list("CHAT_RATE_LIMIT_WHITELIST", ""),
}

# 外部模型接口配置，只用于平台内部教学问答引擎。
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
DEEPSEEK_TIMEOUT_SECONDS = float(
    os.getenv("DEEPSEEK_TIMEOUT_SECONDS", "30")
)
DEEPSEEK_MAX_TOKENS = int(os.getenv("DEEPSEEK_MAX_TOKENS", "800"))
DEEPSEEK_TEMPERATURE = float(os.getenv("DEEPSEEK_TEMPERATURE", "0.2"))

CORS_ALLOW_ORIGINS = _get_origins()

