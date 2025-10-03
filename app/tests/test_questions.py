from __future__ import annotations


def test_create_and_get_question(client):
    r = client.post("/questions/", json={"text": "What is life?"})
    assert r.status_code == 201
    q = r.json()
    assert q["id"] > 0
    assert q["text"] == "What is life?"
    assert "created_at" in q

    r2 = client.get(f"/questions/{q['id']}")
    assert r2.status_code == 200
    detail = r2.json()
    assert detail["id"] == q["id"]
    assert detail["answers"] == []


def test_list_questions_order(client):
    texts = ["A", "B", "C"]
    ids = [client.post("/questions/", json={"text": t}).json()["id"] for t in texts]
    r = client.get("/questions/")
    assert r.status_code == 200
    items = r.json()
    got_ids = [x["id"] for x in items]
    assert got_ids == sorted(ids)


def test_get_question_404(client):
    r = client.get("/questions/999999")
    assert r.status_code == 404


def test_delete_question_404(client):
    r = client.delete("/questions/999999")
    assert r.status_code == 404


def test_question_text_validation(client):
    r = client.post("/questions/", json={"text": ""})
    assert r.status_code == 422
    r = client.post("/questions/", json={"text": "   "})
    assert r.status_code == 422


def test_question_detail_includes_answers(client):
    qid = client.post("/questions/", json={"text": "Q"}).json()["id"]

    a1 = client.post(f"/questions/{qid}/answers/", json={"user_id": "u1", "text": "a1"})
    a2 = client.post(f"/questions/{qid}/answers/", json={"text": "a2"})
    assert a1.status_code == 201 and a2.status_code == 201

    r = client.get(f"/questions/{qid}")
    assert r.status_code == 200
    detail = r.json()
    assert len(detail["answers"]) == 2
    assert all(a["question_id"] == qid for a in detail["answers"])


def test_delete_question_cascades_answers(client):
    qid = client.post("/questions/", json={"text": "Q"}).json()["id"]
    aid = client.post(
        f"/questions/{qid}/answers/", json={"user_id": "u", "text": "A"}
    ).json()["id"]

    r = client.delete(f"/questions/{qid}")
    assert r.status_code == 204

    r2 = client.get(f"/answers/{aid}")
    assert r2.status_code == 404
