import json
import bcrypt
import sqlite3


class userDB:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("user.sqlite", check_same_thread=False)
        self.cursor = self.conn.cursor()

        self.initDB()

    def __del__(self):
        self.conn.close()

    def initDB(self):
        self.cursor.execute(
            """
            SELECT name FROM sqlite_master WHERE type='table' AND name='user'
            """
        )
        if not self.cursor.fetchone():
            self.createTable()

    def createTable(self):
        self.cursor.execute(
            """
            CREATE TABLE user (
                uid INTEGER PRIMARY KEY AUTOINCREMENT,
                id TEXT NOT NULL,
                password TEXT NOT NULL,
                name TEXT NOT NULL,
                admin INTEGER NOT NULL DEFAULT 0,
                etc TEXT NOT NULL
            )
            """
        )
        self.conn.commit()

    def insert(self, id, password, name, admin=0, etc={}):
        if self.exists(id):
            raise Exception("User already exists")

        encryptPassword = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        etc = json.dumps(etc)

        self.cursor.execute(
            """
            INSERT INTO user (uid, id, password, name, admin, etc)
            VALUES (?, ?, ?, ?, ?)
            """,
            (id, encryptPassword, name, admin, etc),
        )
        self.conn.commit()

        return self.getUser(id, password)
    
    def delete(self, id):
        if not self.exists(id):
            raise Exception("User not found")
        
        self.cursor.execute(
            """
            DELETE FROM user WHERE id=?
            """,
            (id,),
        )
        self.conn.commit()

    def exists(self, id):
        self.cursor.execute(
            """
            SELECT * FROM user WHERE id=?
            """,
            (id,),
        )
        user = self.cursor.fetchone()
        if not user:
            return False
        return True

    def getUser(self, id, password):
        self.cursor.execute(
            """
            SELECT * FROM user WHERE id=?
            """,
            (id,),
        )
        user = self.cursor.fetchone()
        if not user:
            raise Exception("User not found")

        if not bcrypt.checkpw(password.encode(), user[2].encode()):
            raise Exception("Password not matched")

        return user

    def setAdmin(self, id, admin):  # 0: user, 1: admin
        self.cursor.execute(
            """
            UPDATE user SET admin=? WHERE id=?
            """,
            (admin, id),
        )
        self.conn.commit()

    def setEtc(self, id, etc: dict):
        etc = json.dumps(etc)

        self.cursor.execute(
            """
            UPDATE user SET etc=? WHERE id=?
            """,
            (etc, id),
        )
        self.conn.commit()

    def updatePassword(self, id, password, newPassword):
        self.getUser(id, password)
        if password == newPassword:
            raise Exception("Password is same")

        newPassword = bcrypt.hashpw(newPassword.encode(), bcrypt.gensalt()).decode()

        self.cursor.execute(
            """
            UPDATE user SET password=? WHERE id=?
            """,
            (newPassword, id),
        )
        self.conn.commit()

    def getAllUsers(self):
        self.cursor.execute(
            """
            SELECT * FROM user
            """
        )
        return self.cursor.fetchall()
