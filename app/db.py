import csv
from dataclasses import dataclass
from operator import itemgetter
from pathlib import Path

from cid import CIDv0, CIDv1, make_cid


@dataclass
class DB:
    csv_path: Path

    def _read(self) -> dict[str, CIDv0 | CIDv1]:
        if not self.csv_path.exists():
            self.csv_path.touch()
            return dict()
        with open(self.csv_path, newline="") as csvfile:
            reader = csv.reader(csvfile)
            return {row[0]: make_cid(row[1]) for row in reader}

    def _write(self, state: dict[str, CIDv0 | CIDv1]) -> None:
        entries = sorted([(k, str(v)) for k, v in state.items()], key=itemgetter(0))
        with open(self.csv_path, "w", newline="") as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerows(entries)

    def put(self, key: str, value: CIDv0 | CIDv1) -> None:
        state = self._read()
        state[key] = value
        self._write(state)

    def get(self, key: str) -> CIDv0 | CIDv1 | None:
        state = self._read()
        return state.get(key, None)
