from db import userDB

userDBC = userDB()


def singleSignup():
    id = input("id: ")
    password = input("password: ")
    name = input("name: ")
    admin = 1

    userDBC.insert(id, password, name, admin)


if __name__ == "__main__":
    print(
        """
        1. Single signup
        """
    )
    choice = int(input("Enter your choice: "))

    if choice == 1:
        singleSignup()
