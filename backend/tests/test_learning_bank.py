"""Exercise the published learning endpoints and grading contracts without Neo4j."""
from decimal import Decimal, localcontext
import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
import pytest

import learning_bank as learning

application = FastAPI()
application.include_router(learning.router)
client = TestClient(application)


def all_questions():
    return learning.bank()["questions"]


def test_six_chapters_have_four_practice_five_exam_and_valid_kp_names():
    response = client.get("/api/learning/chapters")
    assert response.status_code == 200
    chapters = response.json()["data"]["chapters"]
    assert len(chapters) == 6
    snapshot = json.loads((Path(__file__).resolve().parents[2] / "data/graph-snapshot.json").read_text(encoding="utf-8"))
    names = {n["businessId"]: n["properties"]["name"] for n in snapshot["nodes"]}
    for c in chapters:
        assert c["practice_count"] == 4 and c["exam_count"] == 5
        data = client.get(f'/api/learning/chapters/{c["id"]}').json()["data"]
        assert data["lesson"]
        assert len(data["questions"]) == 9
        for q in data["questions"]:
            assert q["main_knowledge_point"]["name"] == names[q["main_knowledge_point"]["id"]]
            assert all(k["name"] == names[k["id"]] for k in q["auxiliary_knowledge_points"])


def test_unsubmitted_questions_do_not_disclose_answers_or_internal_calculation():
    forbidden = {"answer", "correct_answer", "explanation", "option_feedback", "calculation", "expected", "optimal_paths"}
    def inspect(value):
        if isinstance(value, dict):
            assert not (set(value) & forbidden)
            for item in value.values(): inspect(item)
        elif isinstance(value, list):
            for item in value: inspect(item)
    for c in learning.bank()["chapters"]:
        inspect(client.get(f'/api/learning/chapters/{c["id"]}').json())


@pytest.mark.parametrize("q", all_questions(), ids=lambda q: q["id"])
def test_all_54_published_answers_grade_as_correct_with_complete_feedback(q):
    value = q["answer"]["value"] if q["type"] == "numeric" else q["answer"]
    result = learning.grade(q, value)
    assert result["correct"] is True
    assert result["explanation"] and result["sources"]
    assert len(result["option_feedback"]) == len(q["options"])


@pytest.mark.parametrize("q", [q for q in all_questions() if q["type"] == "multiple"], ids=lambda q: q["id"])
def test_multiple_choice_exact_set_no_missing_extra_or_duplicate(q):
    assert learning.grade(q, list(reversed(q["answer"])))["correct"] is True
    assert learning.grade(q, q["answer"][:-1])["correct"] is False
    extra = next(o["id"] for o in q["options"] if o["id"] not in q["answer"])
    assert learning.grade(q, q["answer"] + [extra])["correct"] is False
    with pytest.raises(HTTPException): learning.grade(q, q["answer"] + [q["answer"][0]])


@pytest.mark.parametrize("q", [q for q in all_questions() if q["type"] == "numeric"], ids=lambda q: q["id"])
def test_numeric_inclusive_tolerance_and_nonfinite_rejection(q):
    answer = q["answer"]
    value = Decimal(str(answer["value"])); tolerance = Decimal(str(answer["tolerance"]))
    for candidate in [value, value + tolerance, value - tolerance]:
        assert learning.grade(q, str(candidate))["correct"] is True
    for candidate in [value + tolerance * 2, value - tolerance * 2]:
        assert learning.grade(q, str(candidate))["correct"] is False
    # A tiny excess must not round back onto the inclusive boundary.
    with localcontext() as context:
        context.prec = 80
        just_outside = value + tolerance + Decimal('1e-40')
        assert learning.grade(q, str(just_outside))["correct"] is False
    for invalid in [True, None, "NaN", "Infinity", "2+3", "500米", {"value": answer["value"], "unit": "wrong"}]:
        with pytest.raises(HTTPException): learning.grade(q, invalid)


def test_false_is_not_misread_as_blank_or_zero():
    q = next(q for q in all_questions() if q["type"] == "true_false" and q["answer"] is False)
    assert learning.grade(q, False)["correct"] is True
    for wrong_type in [0, "false", None]:
        with pytest.raises(HTTPException): learning.grade(q, wrong_type)


def test_practice_cannot_fetch_exam_answer_by_submitting_exam_id():
    r = client.post("/api/learning/chapters/L01/practice", json={"question_id": "L01-E01", "answer": "B"})
    assert r.status_code == 400
    assert "correct_answer" not in r.json()


def test_exam_complete_submission_80_pass_60_fail_and_reject_wrong_chapter_ids():
    qs = learning.questions("L01", "exam")
    answers = {q["id"]: q["answer"] for q in qs}
    url = "/api/learning/chapters/L01/exam"
    assert client.post(url, json={"answers": {}}).status_code == 400
    all_correct = client.post(url, json={"answers": answers}).json()["data"]
    assert all_correct["score"] == 100 and all_correct["passed"] is True
    first = qs[0]
    answers[first["id"]] = next(o["id"] for o in first["options"] if o["id"] != first["answer"])
    result = client.post(url, json={"answers": answers}).json()["data"]
    assert result["score"] == 80 and result["passed"] is True
    second = qs[1]
    answers[second["id"]] = [second["answer"][0]]
    result = client.post(url, json={"answers": answers}).json()["data"]
    assert result["score"] == 60 and result["passed"] is False
    assert len(result["results"]) == 5
    answers["L02-E01"] = answers.pop("L01-E01")
    assert client.post(url, json={"answers": answers}).status_code == 400


def test_unknown_chapter_and_invalid_numeric_answer():
    assert client.get('/api/learning/chapters/unknown').status_code == 404
    r = client.post('/api/learning/chapters/L02/practice', json={"question_id": "L02-P04", "answer": "NaN"})
    assert r.status_code == 400
