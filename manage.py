import os
import json
import string
import os.path as osp
from config import *

class Manage:
    def __init__(self):
        self.path = osp.join("/", "home", "pi", "configs")

    def getPeers(self):
        return os.listdir(self.path)

    def getPeer(self, uid):
        if not uid.endswith(".conf"):
            uid += ".conf"

        if uid in self.getPeers():
            with open(osp.join(self.path, uid)) as f:
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

    def addPeer(self, uid):
        peerAddReturn = os.system(f"pivpn add -n infosec_{uid}")

        if not peerAddReturn:
            return True
        raise Exception("Peer not added")

    def removePeer(self, uid):
        peerRemoveReturn = os.system(f"pivpn remove -y infosec_{uid}")

        if not peerRemoveReturn:
            return True
        raise Exception("Peer not removed")


if __name__ == "__main__":
    m = Manage()
    for peer in m.getPeers():
        print(m.getPeer(peer))
