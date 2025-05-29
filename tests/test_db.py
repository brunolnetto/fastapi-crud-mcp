# tests/test_db.py
from sqlalchemy.orm import Session

from backend.server.db import get_db

def test_get_db():
    # Create a generator from get_db
    db_generator = get_db()
    # Retrieve the session from the generator
    db_session = next(db_generator)
    assert isinstance(db_session, Session)
    # Close the session by advancing the generator
    try:
        next(db_generator)
    except StopIteration:
        pass
