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
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                name TEXT NOT NULL,
                admin INTEGER NOT NULL DEFAULT 0,
                confirmed INTEGER NOT NULL DEFAULT 0,
                etc TEXT,
                UNIQUE(email)
            )
            """
        )
        self.conn.commit()

    def insert(self, email, password, name, admin=0, confirmed=0, etc={}, studentId=""):
        if self.exists(email):
            raise Exception("User already exists")

        if etc == {}:
            etc["studentId"] = studentId

        encryptPassword = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        etc = json.dumps(etc)

        self.cursor.execute(
            """
            INSERT INTO user (email, password, name, admin, confirmed, etc)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (email, encryptPassword, name, admin, confirmed, etc),
        )
        self.conn.commit()

        return self.getUser(email, password)

    def exists(self, email):
        self.cursor.execute(
            """
            SELECT * FROM user WHERE email=?
            """,
            (email,),
        )
        user = self.cursor.fetchone()
        if not user:
            return False
        return True

    def getUser(self, email, password):
        self.cursor.execute(
            """
            SELECT * FROM user WHERE email=?
            """,
            (email,),
        )
        user = self.cursor.fetchone()
        if not user:
            raise Exception("User not found")

        if not bcrypt.checkpw(password.encode(), user[2].encode()):
            raise Exception("Password not matched")

        return user

    def setAdmin(self, email, admin):
        self.cursor.execute(
            """
            UPDATE user SET admin=? WHERE email=?
            """,
            (admin, email),
        )
        self.conn.commit()

    def setConfirmed(self, email, confirmed):
        self.cursor.execute(
            """
            UPDATE user SET confirmed=? WHERE email=?
            """,
            (confirmed, email),
        )
        self.conn.commit()

    def setEtc(self, email, etc: dict):
        etc = json.dumps(etc)

        self.cursor.execute(
            """
            UPDATE user SET etc=? WHERE email=?
            """,
            (etc, email),
        )
        self.conn.commit()
