from models.user import User
from sqlalchemy import exc
from db import session
from models.tablecreator import User_query

class Users:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def singup(self):
        try:
            new_user = User(username=self.username,password=self.password)
            session.add(new_user)
            session.commit()
            user_id = User_query().return_user_id_by_username(self.username)
            return user_id
        except exc.IntegrityError:
            session.rollback()
            return None

    def login(self):
        query = session.query(User).filter(User.username == self.username).first()
        if self.password == query.password:
            return query.id