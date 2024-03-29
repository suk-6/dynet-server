import os
import json
import string
import os.path as osp
from config import *
from functools import wraps


def namefilter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        uuid = kwargs.get("uuid")
        if not uuid:
            raise Exception("No uuid provided")
        if not all(c in string.ascii_letters + string.digits + "-_@." for c in uuid):
            raise Exception("uuid contains invalid characters")
        return func(*args, **kwargs)

    return wrapper


class Manage:
    def __init__(self):
        self.path = osp.join("/", "home", "pi", "configs")

    def getPeers(self):
        return os.listdir(self.path)

    def getPeer(self, uuid):
        if not uuid.endswith(".conf"):
            uuid += ".conf"

        if uuid in self.getPeers():
            with open(osp.join(self.path, uuid)) as f:
                data = f.read().split("\n")

                return json.dumps(
                    {
                        "privateKey": data[1].split(" = ")[1],
                        "address": data[2].split(" = ")[1],
                        "publicKey": data[6].split(" = ")[1],
                        "presharedKey": data[7].split(" = ")[1],
                        "endpoint": ENDPOINT,
                        "allowedIPs": ALLOWEDIPS,
                        "dns": DNS,
                    }
                )

        raise Exception("Peer not found")

    @namefilter
    def addPeer(self, uuid):
        os.system(f"pivpn add -n {uuid}")

        if f"{uuid}.conf" in self.getPeers():
            return True
        raise Exception("Peer not added")

    @namefilter
    def removePeer(self, uuid):
        os.system(f"pivpn remove -y {uuid}")

        if f"{uuid}.conf" not in self.getPeers():
            return True
        raise Exception("Peer not removed")


if __name__ == "__main__":
    m = Manage()
    for peer in m.getPeers():
        print(m.getPeer(peer))
