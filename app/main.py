from io import BytesIO
from pathlib import Path
import typer
from cid import make_cid
from linked_list import Linked, Node, print_node

from ipfs_infura import IPFSInfura
from db import DB

PROJECT_ID = "2K8bGGM5QCnBSoUuEUEA9qrGgbl"
PROJECT_SECRET = "c3aad3ee1011afc48142a8e33eaccd92"
PROVIDER_ENDPOINT = "https://ipfs.infura.io:5001"

cli = typer.Typer()
infura = IPFSInfura(PROJECT_ID, PROJECT_SECRET, PROVIDER_ENDPOINT)
db = DB(Path("db.csv"))
linked = Linked(infura)


@cli.command()
def cat(hash: str, verbose: bool = True):
    cid = make_cid(hash)
    content = infura.cat(cid)
    print("Got file", hash)
    if verbose:
        print(content.decode("utf-8"))


@cli.command()
def add(content: str):
    cid = infura.add(BytesIO(content.encode("utf-8")))
    print("Add", str(cid))


@cli.command()
def unpin(hash: str, verbose: bool = True):
    cid = make_cid(hash)
    infura.unpin(cid)
    print("Unpinned", hash)


@cli.command()
def append(key: str, content: str = typer.Option(..., prompt=True)):
    # print("content", content)
    parent_cid = db.get(key)
    new_node = Node(parent=parent_cid, content=content.encode("utf-8"))
    # print("new_parent ", new_node.parent)
    # print("node_encoded", new_node.encode())
    new_cid = linked.create(new_node)
    # print("new_cid    ", new_cid)
    db.put(key, new_cid)
    print_node(new_node, new_cid, True)


@cli.command()
def traverse(key: str, verbose: bool = True):
    next_cid = db.get(key)
    if next_cid is None:
        print("No node found")
        return
    for node in linked.iternodes(next_cid):
        assert next_cid is not None
        print_node(node, next_cid, verbose)
        next_cid = node.parent


if __name__ == "__main__":
    cli()
