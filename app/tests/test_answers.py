from __future__ import annotations


def _mk_question(client, text="Q"):
    return client.post("/questions/", json={"text": text}).json()["id"]


def test_create_answer_for_existing_question(client):
    qid = _mk_question(client)
    r = client.post(
        f"/questions/{qid}/answers/", json={"user_id": "bob", "text": "hello"}
    )
    assert r.status_code == 201
    a = r.json()
    assert a["question_id"] == qid
    assert a["user_id"] == "bob"
    assert a["text"] == "hello"


def test_create_answer_for_missing_question(client):
    r = client.post("/questions/999999/answers/", json={"user_id": "u", "text": "x"})
    assert r.status_code == 400


def test_get_and_delete_answer(client):
    qid = _mk_question(client)
    aid = client.post(
        f"/questions/{qid}/answers/", json={"user_id": "u1", "text": "t"}
    ).json()["id"]

    r = client.get(f"/answers/{aid}")
    assert r.status_code == 200
    assert r.json()["id"] == aid

    r2 = client.delete(f"/answers/{aid}")
    assert r2.status_code == 204

    r3 = client.get(f"/answers/{aid}")
    assert r3.status_code == 404


def test_trim_and_validation(client):
    qid = _mk_question(client)

    r_ok = client.post(
        f"/questions/{qid}/answers/", json={"user_id": "  alice ", "text": "  hey  "}
    )
    assert r_ok.status_code == 201
    a = r_ok.json()
    assert a["user_id"] == "alice"
    assert a["text"] == "hey"

    r_bad = client.post(f"/questions/{qid}/answers/", json={"user_id": "u", "text": ""})
    assert r_bad.status_code == 422


def test_generate_user_id_if_missing_or_blank(client):
    qid = _mk_question(client)

    r1 = client.post(f"/questions/{qid}/answers/", json={"text": "x"})
    assert r1.status_code == 201
    assert r1.json()["user_id"] and isinstance(r1.json()["user_id"], str)

    r2 = client.post(f"/questions/{qid}/answers/", json={"user_id": "   ", "text": "y"})
    assert r2.status_code == 201
    assert r2.json()["user_id"] and isinstance(r2.json()["user_id"], str)
