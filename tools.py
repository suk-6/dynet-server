from db import userDB
from manage import Manage

userDBC = userDB()
vpnManage = Manage()


def singleSignup():
    id = input("id: ")
    password = input("password: ")
    name = input("name: ")
    admin = 1
    userDBC.insert(id, password, name, admin)

    user = userDBC.getUser(id, password)
    vpnManage.addPeer(uid=user[0])


if __name__ == "__main__":
    print(
        """
        1. Single signup
        """
    )
    choice = int(input("Enter your choice: "))

    if choice == 1:
        singleSignup()
