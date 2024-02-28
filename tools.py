from db import userDB

userDBC = userDB()


if __name__ == "__main__":
    id = input("id: ")
    password = input("password: ")
    name = input("name: ")
    admin = 1

    userDBC.insert(id, password, name, admin)
