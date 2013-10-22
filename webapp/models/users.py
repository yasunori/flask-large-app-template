from sqlalchemy import Column, Integer, String, Text, DateTime
from webapp.models.database import db_session
from webapp.models.database import Base
from webapp.models.models import ModelsBase, ModelManager


class Users(ModelsBase,Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login_id = Column(Text)
    password = Column(Text)

    def __repr__(self):
        return '<Title %r>' % (self.login_id)


class UsersManager(ModelManager):

    def get_model(self):
        return Users

    def __init__(self):
        pass

    def check_exists(self,login_id):
        where = (Users.login_id == login_id)
        cnt = self.select_count(where)
        if(cnt >= 1):
            return True
        return False
