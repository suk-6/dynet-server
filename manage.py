import os
import string
import os.path as osp
from functools import wraps


def namefilter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        email = kwargs.get("email")
        if not email:
            raise Exception("No email provided")
        if not all(c in string.ascii_letters + string.digits + "-_@." for c in email):
            raise Exception("Email contains invalid characters")
        return func(*args, **kwargs)

    return wrapper


class Manage:
    def __init__(self):
        self.path = osp.join("/", "home", "pi", "configs")

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
    def addPeer(self, email):
        os.system(f"pivpn add -n {email}")

        if f"{email}.conf" in self.getPeers():
            return True
        raise Exception("Peer not added")

    @namefilter
    def removePeer(self, email):
        os.system(f"pivpn remove -y {email}")

        if f"{email}.conf" not in self.getPeers():
            return True
        raise Exception("Peer not removed")


if __name__ == "__main__":
    m = Manage()
    for peer in m.getPeers():
        print(m.getPeer(peer))
