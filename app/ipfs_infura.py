from dataclasses import dataclass
from io import BytesIO
from cid import CIDv0, CIDv1, make_cid

import requests


@dataclass
class IPFSInfura:
    project_id: str
    project_secret: str
    provider_endpoint: str

    def add(self, data: BytesIO | bytes, pin: bool = True) -> CIDv0 | CIDv1:
        files = {"file": data}
        resp = requests.post(
            f"{self.provider_endpoint}/api/v0/add",
            files=files,
            params={"pin": "true" if pin else "false"},
            auth=(self.project_id, self.project_secret),
        )
        assert resp.status_code == 200
        j = resp.json()
        return make_cid(j["Hash"])

    def cat(self, cid: CIDv0 | CIDv1) -> bytes:
        resp = requests.post(
            f"{self.provider_endpoint}/api/v0/cat",
            params={"arg": str(cid)},
            auth=(self.project_id, self.project_secret),
        )
        assert resp.status_code == 200
        return resp.content

    def pin(self, cid: CIDv0 | CIDv1) -> None:
        requests.post(
            f"{self.provider_endpoint}/api/v0/pin/add",
            params={"arg": str(cid)},
            auth=(self.project_id, self.project_secret),
        )

    def unpin(self, cid: CIDv0 | CIDv1) -> None:
        resp = requests.post(
            f"{self.provider_endpoint}/api/v0/pin/rm",
            params={"arg": str(cid)},
            auth=(self.project_id, self.project_secret),
        )
        assert resp.status_code == 200
