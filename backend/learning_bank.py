"""Six introductory chapters, public question views and deterministic grading.

Answers stay on the server until a practice answer or a complete exam is submitted.
This is an anonymous self-study tool; progress is stored by the browser.
"""
from decimal import Decimal, InvalidOperation
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
import json
import re
import unicodedata
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

CONTENT_PATH = Path(__file__).resolve().parent / "content" / "learning-bank.json"
router = APIRouter(prefix="/api/learning", tags=["learning"])


@lru_cache(maxsize=1)
def bank():
    data = json.loads(CONTENT_PATH.read_text(encoding="utf-8"))
    if len(data["chapters"]) != 6 or len(data["questions"]) != 54:
        raise ValueError("学习内容数量不完整")
    return data


def chapter(chapter_id):
    item = next((c for c in bank()["chapters"] if c["id"] == chapter_id), None)
    if item is None:
        raise HTTPException(404, "没有找到这一关")
    return item


def questions(chapter_id, category=None):
    chapter(chapter_id)
    return [q for q in bank()["questions"] if q["chapter_id"] == chapter_id
            and (category is None or q["category"] == category)]


def references(evidence):
    sources = {s["id"]: s for s in bank()["sources"]}
    return [{"id": e["source_id"], "title": sources[e["source_id"]]["title"],
             "url": sources[e["source_id"]]["url"], "section": e["section"],
             "support": e["support"]} for e in evidence]


def public_question(q):
    result = {k: q[k] for k in ("id", "type", "category", "stem", "options",
                                "learning_objective", "main_knowledge_point",
                                "auxiliary_knowledge_points")}
    if q["type"] == "numeric":
        result["numeric"] = {"unit": q["answer"]["unit"],
                             "tolerance": q["answer"]["tolerance"]}
    if q.get("diagram_mermaid"):
        c = q["calculation"]
        result["diagram"] = {"edges": c["inputs"]["edges"],
                             "blocked": c["inputs"]["blocked"], "unit": c["unit"]}
    return result


def public_chapter(c, include_questions=False):
    qs = questions(c["id"])
    points = {}
    for q in qs:
        for kp in [q["main_knowledge_point"]] + q["auxiliary_knowledge_points"]:
            points[kp["id"]] = kp
    result = {"id": c["id"], "title": c["title"], "objectives": c["objectives"],
              "prerequisites": c["prerequisite_chapters"],
              "practice_count": sum(q["category"] == "practice" for q in qs),
              "exam_count": sum(q["category"] == "exam" for q in qs),
              "knowledge_points": list(points.values())}
    if include_questions:
        # Drop author-facing comments; preserve all actual teaching conditions.
        lesson = c["teaching_card"].replace("此短卡补足原知识图谱中通用GIS基础较分散的讲解。", "")
        lesson = lesson.replace("本卡明确补正M4-006缺失条件，须先讲后测。", "先理解这些条件，再开始练习。")
        result.update(lesson=lesson, questions=[public_question(q) for q in qs])
    return result


def normalized_answer(q, answer):
    kind = q["type"]
    valid_options = {o["id"] for o in q["options"]}
    error = HTTPException(400, "答案格式不正确，请按本题题型填写")
    if kind == "single":
        if type(answer) is not str or answer not in valid_options:
            raise error
        return answer
    if kind == "multiple":
        if (type(answer) is not list or not answer or len(answer) > len(valid_options)
                or any(type(x) is not str or x not in valid_options for x in answer)
                or len(answer) != len(set(answer))):
            raise error
        return sorted(answer)
    if kind == "true_false":
        if type(answer) is not bool:
            raise error
        return answer
    if type(answer) not in (int, float, str):
        raise error
    value = unicodedata.normalize("NFKC", str(answer)).strip()
    if len(value) > 64 or not re.fullmatch(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d{1,3})?", value):
        raise HTTPException(400, "请输入有限数值，例如3.6；单位使用题目指定单位")
    try:
        number = Decimal(value)
        if not number.is_finite():
            raise error
        return number
    except InvalidOperation:
        raise error


def grade(q, answer):
    actual = normalized_answer(q, answer)
    expected = q["answer"]
    if q["type"] == "numeric":
        correct = abs(Fraction(actual) - Fraction(str(expected["value"]))) <= Fraction(str(expected["tolerance"]))
        actual = str(actual)
    elif q["type"] == "multiple":
        correct = actual == sorted(expected)
    else:
        correct = type(actual) is type(expected) and actual == expected
    return {"question_id": q["id"], "correct": correct, "submitted_answer": actual,
            "correct_answer": expected, "explanation": q["explanation"],
            "option_feedback": q["option_feedback"], "sources": references(q["evidence"]),
            "main_knowledge_point": q["main_knowledge_point"]}


class PracticeSubmission(BaseModel):
    question_id: str = Field(min_length=1, max_length=32)
    answer: Any


class ExamSubmission(BaseModel):
    answers: Dict[str, Any]


@router.get("/chapters")
def list_chapters():
    return {"code": 200, "data": {"version": bank()["content_version"],
            "pass_score": 80, "points_per_exam_question": 20,
            "chapters": [public_chapter(c) for c in bank()["chapters"]]}}


@router.get("/chapters/{chapter_id}")
def get_chapter(chapter_id: str):
    return {"code": 200, "data": public_chapter(chapter(chapter_id), include_questions=True)}


@router.post("/chapters/{chapter_id}/practice")
def submit_practice(chapter_id: str, submission: PracticeSubmission):
    q = next((q for q in questions(chapter_id, "practice")
              if q["id"] == submission.question_id), None)
    if q is None:
        raise HTTPException(400, "这道题不属于本关练习")
    return {"code": 200, "data": grade(q, submission.answer)}


@router.post("/chapters/{chapter_id}/exam")
def submit_exam(chapter_id: str, submission: ExamSubmission):
    qs = questions(chapter_id, "exam")
    if set(submission.answers) != {q["id"] for q in qs}:
        raise HTTPException(400, "请完成本关全部5道考试题后交卷")
    results = [grade(q, submission.answers[q["id"]]) for q in qs]
    correct_count = sum(r["correct"] for r in results)
    score = correct_count * 20
    return {"code": 200, "data": {"chapter_id": chapter_id, "score": score,
            "total": 100, "correct_count": correct_count, "question_count": len(qs),
            "passed": score >= 80, "results": results}}
