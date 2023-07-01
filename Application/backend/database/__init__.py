import mysql.connector

class veritabani():
    def __init__(self, islem=None, access=None, secret=None, user=None, password=None, userid=None):
        self.db = mysql.connector.connect(
            host="localhost",
            user="barron4335",
            password="1968Hram",
            database="alsatbot"
        )

        self.cursor = self.db.cursor(dictionary=True)

        if islem == "acces_secret_key_control":
            sql = "SELECT * FROM pac_log WHERE pac_log_access_key = %s AND pac_log_secret_key = %s"
            self.cursor.execute(sql, (access, secret))
            asvarmi = self.cursor.fetchone()
            if asvarmi:
                return True

            else:
                return False

        elif islem == "log_user_id":
            sql = "SELECT pac_log_user_id FROM pac_log WHERE pac_log_access_key = %s AND pac_log_secret_key = %s"
            self.cursor.execute(sql, (access, secret, ))
            uservarmi = self.cursor.fetchone()
            uservarmi = uservarmi['pac_log_user_id']
            return uservarmi

        elif islem == "user_log_checking":
            sql = "SELECT * FROM users WHERE user_name = %s AND user_password = %s AND user_id = %s"
            self.cursor.execute(sql, (user, password, userid))
            userlogvarmi = self.cursor.fetchall()
            if userlogvarmi:
                return True
            else:
                return False

        elif islem == "user_data":
            sql = "SELECT * FROM users WHERE user_name = %s AND user_password = %s AND user_id = %s"
            self.cursor.execute(sql, (user, password, userid))
            userlogvarmi = self.cursor.fetchall()
            return userlogvarmi