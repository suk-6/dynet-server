import os
import string
import os.path as osp
from functools import wraps
from dotenv import load_dotenv

load_dotenv()


def namefilter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        name = kwargs.get("name")
        if not name:
            raise Exception("No name provided")
        if not all(c in string.ascii_letters + string.digits + "-" for c in name):
            raise Exception("Name contains invalid characters")
        return func(*args, **kwargs)

    return wrapper


class Manage:
    def __init__(self):
        # self.path = osp.join("/", "home", "pi", "configs")
        self.path = osp.join("configs")

    def getPeers(self):
        return os.listdir(self.path)

    def getPeer(self, peer):
        if not peer.endswith(".conf"):
            peer += ".conf"

        if peer in self.getPeers():
            with open(osp.join(self.path, peer)) as f:
                return f.read()
        raise Exception("Peer not found")

    @namefilter
    def addPeer(self, name):
        os.system(f"pivpn add -n {name}")

        if f"{name}.conf" in self.getPeers():
            return True
        raise Exception("Peer not added")

    @namefilter
    def removePeer(self, name):
        os.system(f"pivpn remove -y {name}")

        if f"{name}.conf" not in self.getPeers():
            return True
        raise Exception("Peer not removed")


if __name__ == "__main__":
    m = Manage()
    for peer in m.getPeers():
        print(m.getPeer(peer))