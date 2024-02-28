import os
import string
import os.path as osp
from functools import wraps


def namefilter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        uid = kwargs.get("uid")
        if not uid:
            raise Exception("No uid provided")
        if not all(c in string.ascii_letters + string.digits + "-_@." for c in uid):
            raise Exception("Uid contains invalid characters")
        return func(*args, **kwargs)

    return wrapper


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
                return f.read()
        raise Exception("Peer not found")

    @namefilter
    def addPeer(self, uid):
        os.system(f"pivpn add -n {uid}")

        if f"{uid}.conf" in self.getPeers():
            return True
        raise Exception("Peer not added")

    @namefilter
    def removePeer(self, uid):
        os.system(f"pivpn remove -y {uid}")

        if f"{uid}.conf" not in self.getPeers():
            return True
        raise Exception("Peer not removed")


if __name__ == "__main__":
    m = Manage()
    for peer in m.getPeers():
        print(m.getPeer(peer))
