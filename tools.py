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
    vpnManage.addPeer(id=id)

def showAllUsers():
    users = userDBC.getAllUsers()
    for user in users:
        print(user)

def multiSignup(prefix, password, start=1, count=10):
    for i in range(start, start + count):
        id = f"{prefix}{i}"
        name = f"{prefix}{i}"
        admin = 0
        userDBC.insert(id, password, name, admin)

        user = userDBC.getUser(id, password)
        vpnManage.addPeer(uid=user[0])

def removeUser(id):
    user = userDBC.getUser(id, "password")
    vpnManage.removePeer(id=id)
    userDBC.delete(id)


if __name__ == "__main__":
    print(
        """
        1. Single signup
        2. Show all users
        3. Multi signup
        4. Remove user
        """
    )
    choice = int(input("Enter your choice: "))

    if choice == 1:
        singleSignup()
    elif choice == 2:
        showAllUsers()
    elif choice == 3:
        prefix = input("Prefix: ") # ex) user
        start = input("Start number: ") # ex) 1
        count = input("Count: ") # ex) 10
        password = input("Password: ")
        multiSignup(prefix, password, int(start), int(count))
    elif choice == 4:
        id = input("id: ")
        removeUser(id)
