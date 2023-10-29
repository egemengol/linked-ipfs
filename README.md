
An append-only, IPFS backend linked list implementation

Designed to hold a binary blob as payload, the schema is left to application.

Requires Infura for pinning the entities on IPFS.  
Requires a database for keeping the CID of the latest node.

CLI prompts user to enter a string, which is then set as the payload for a node.

The nodes in the example below produce a tree.
The list is acquired by traversing back from a known leaf.
Eliminates the need for authentication.

```sh
❯ python app/main.py append egemen
Content: first
                                Node        QmPZGW8VEyztHgua36xH8k8pwBUMs1PUeMKegp1Mdr8coj
                                with parent None
first


❯ python app/main.py append egemen
Content: second message is longg
                                Node        QmSi6GqX1sNaMLoZmqVrtMoTQTccmD5LaCNLUEi3Xx4ZEv
                                with parent QmPZGW8VEyztHgua36xH8k8pwBUMs1PUeMKegp1Mdr8coj
second message is longg


❯ python app/main.py append deniz
Content: first again
                                Node        QmQno79wZ1F4riyyLhCdjqiD7s6u6p4DZTcnKEWYrtSDjr
                                with parent None
first again


❯ python app/main.py traverse deniz
                                Node        QmQno79wZ1F4riyyLhCdjqiD7s6u6p4DZTcnKEWYrtSDjr
                                with parent None
first again


❯ python app/main.py traverse egemen
                                Node        QmSi6GqX1sNaMLoZmqVrtMoTQTccmD5LaCNLUEi3Xx4ZEv
                                with parent QmPZGW8VEyztHgua36xH8k8pwBUMs1PUeMKegp1Mdr8coj
second message is longg

                                Node        QmPZGW8VEyztHgua36xH8k8pwBUMs1PUeMKegp1Mdr8coj
                                with parent None
first

```
