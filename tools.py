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
    vpnManage.addPeer(uuid=user[0])

def showAllUsers():
    users = userDBC.getAllUsers()
    for user in users:
        print(user)


if __name__ == "__main__":
    print(
        """
        1. Single signup
        2. Show all users
        """
    )
    choice = int(input("Enter your choice: "))

    if choice == 1:
        singleSignup()
    elif choice == 2:
        showAllUsers()
