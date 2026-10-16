# Copyright (c) 2026 ?????
# GIS???????????? - ????
# ?????????????????????

# Copyright (c) 2026 版权所有人
# GIS交通路网教学知识图谱平台 - 后端服务
# 本文件为平台核心业务代码，受软件著作权保护

import logging
from typing import Any, Dict

from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI

import prompt_engine
from config import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    DEEPSEEK_MAX_TOKENS,
    DEEPSEEK_MODEL,
    DEEPSEEK_TEMPERATURE,
    DEEPSEEK_TIMEOUT_SECONDS,
    QA_CONFIG,
)


logger = logging.getLogger(__name__)


class QaEngineConfigError(RuntimeError):
    pass


class QaEngineRequestError(RuntimeError):
    pass


# 兼容旧接口，避免已有调用方失效。
DeepSeekConfigurationError = QaEngineConfigError
DeepSeekRequestError = QaEngineRequestError


def is_configured() -> bool:
    return bool(DEEPSEEK_API_KEY.strip())


def get_status() -> Dict[str, Any]:
    return {
        "configured": is_configured(),
        "model": DEEPSEEK_MODEL,
        "engine": "GIS交通路网教学问答引擎",
        "message": (
            "GIS交通路网教学知识图谱问答引擎已配置"
            if is_configured()
            else "GIS交通路网教学知识图谱问答引擎尚未配置API Key"
        ),
    }


def _create_client() -> OpenAI:
    return OpenAI(
        api_key=DEEPSEEK_API_KEY.strip(),
        base_url=DEEPSEEK_BASE_URL,
        timeout=DEEPSEEK_TIMEOUT_SECONDS,
    )


def teaching_qa(
    question: str,
    graph_context: Dict[str, Any],
) -> Dict[str, Any]:
    if not is_configured():
        raise QaEngineConfigError(
            "GIS交通路网教学知识图谱问答引擎尚未配置API Key。"
        )

    prompt_package = prompt_engine.build_prompt(
        question,
        graph_context,
        max_references=QA_CONFIG["max_references"],
    )
    client = _create_client()

    try:
        response = client.chat.completions.create(
            model=DEEPSEEK_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": prompt_package.system_prompt,
                },
                {
                    "role": "user",
                    "content": prompt_package.user_prompt,
                },
            ],
            temperature=DEEPSEEK_TEMPERATURE,
            max_tokens=DEEPSEEK_MAX_TOKENS,
        )
    except APITimeoutError as exc:
        raise QaEngineRequestError(
            "GIS交通路网教学知识图谱问答引擎请求超时。"
        ) from exc
    except APIConnectionError as exc:
        raise QaEngineRequestError(
            "GIS交通路网教学知识图谱问答引擎无法连接外部模型服务。"
        ) from exc
    except APIStatusError as exc:
        logger.warning("External teaching QA status error: %s", exc)
        raise QaEngineRequestError(
            "GIS交通路网教学知识图谱问答引擎服务状态异常。"
        ) from exc
    except Exception as exc:
        logger.exception("Unexpected teaching QA request error")
        raise QaEngineRequestError(
            "GIS交通路网教学知识图谱问答引擎调用失败。"
        ) from exc

    if not response.choices:
        raise QaEngineRequestError("教学问答引擎未返回有效回答。")

    content = response.choices[0].message.content
    try:
        validated_answer = prompt_engine.validate_answer(
            content or "",
            prompt_package,
        )
    except ValueError as exc:
        raise QaEngineRequestError(str(exc)) from exc

    references = prompt_engine.matched_references(
        validated_answer,
        prompt_package.context_nodes,
    )
    return {
        "answer": validated_answer,
        "scene": prompt_package.scene,
        "references": references,
    }


def answer_question(question: str, graph_context: Dict[str, Any]) -> str:
    """兼容旧调用方式，仅返回答案文本。"""
    return str(teaching_qa(question, graph_context)["answer"])

