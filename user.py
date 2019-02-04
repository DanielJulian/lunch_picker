from flask_login import UserMixin
from database_tools import get_db


class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.voted = False

    def __repr__(self):
        return "%d/%s" % (self.id, self.voted)


def validate_user(username, password):
    db = get_db()
    cur = db.cursor()
    query = "SELECT * FROM user WHERE email='%s' AND password='%s'" % (username, password)
    cur.execute(query)
    result = cur.fetchall()
    if len(result) > 0:
        return result[0]
    else:
        return False
