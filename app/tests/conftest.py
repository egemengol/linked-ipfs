from pathlib import Path
import pytest
from app.db import DB


@pytest.fixture(scope="function")
def db():
    db_path = Path("app/tests/db.csv")
    db_path.unlink(missing_ok=True)
    return DB(db_path)
