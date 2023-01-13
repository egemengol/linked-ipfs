from dataclasses import dataclass
from io import BytesIO

from cid import CIDv0, CIDv1, make_cid

from ipfs_infura import IPFSInfura


def int_to_byte(n: int) -> bytes:
    return n.to_bytes(1, byteorder="big", signed=False)


def byte_to_int(b: bytes) -> int:
    return int.from_bytes(b, byteorder="big", signed=False)


@dataclass
class Node:
    parent: CIDv0 | CIDv1 | None
    content: bytes

    @classmethod
    def decode(cls, outer: bytes):
        b = BytesIO(outer)
        length = byte_to_int(b.read(1))
        parent_cid = None
        if length:
            parent_cid = make_cid(b.read(length))

        inner = b.read()
        return cls(parent_cid, inner)

    def encode(self) -> bytes:
        outer = BytesIO()
        if self.parent is None:
            outer.write(int_to_byte(0))
        else:
            parent_encoded = self.parent.encode()
            length = len(parent_encoded)
            outer.write(int_to_byte(length))
            outer.write(parent_encoded)

        outer.write(self.content)

        return outer.getvalue()


def print_node(node: Node, cid: CIDv0 | CIDv1, print_content: bool = True):
    print("\t\t\t\tNode       ", str(cid))
    print("\t\t\t\twith parent", str(node.parent))
    if print_content:
        print(node.content.decode("utf-8"))
    print()


@dataclass
class Linked:
    infura: IPFSInfura

    def get(self, cid: CIDv0 | CIDv1) -> Node | None:
        node_encoded = self.infura.cat(cid)
        node = Node.decode(node_encoded)
        return node

    def iternodes(self, cid: CIDv0 | CIDv1):
        next_cid: CIDv0 | CIDv1 | None = cid
        while True:
            if next_cid is None:
                break
            node = self.get(next_cid)
            assert node is not None
            next_cid = node.parent
            yield node

    def create(self, node: Node) -> CIDv0 | CIDv1:
        node_encoded = node.encode()
        cid = self.infura.add(node_encoded)
        return cid
