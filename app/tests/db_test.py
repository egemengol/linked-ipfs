from app.db import DB
from cid import make_cid


def test_db(db: DB):
    assert db._read() == dict()

    key = "egemen"
    value = make_cid("QmeEGnfiixmBwvTr1q3hN7ZndmuefJASv95CpJgN3rYa8h")
    assert db.get(key) is None

    db.put(key, value)
    assert db.get(key) == value

    value = make_cid("QmS1MQyu7ZiuU26JjQYMtRtZxZmhP7q6BHGZXRYFSPCEjs")
    db.put(key, value)
    assert db.get(key) == value

    assert db._read() == {key: value}

    key_2 = "ahmet"
    value_2 = make_cid("QmYr2gZL82HDwzm8AkZqFFHMetAfjR6YSuiqXcUghco7mJ")
    db.put(key_2, value_2)

    assert db._read() == {
        key: value,
        key_2: value_2,
    }
