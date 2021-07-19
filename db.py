from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db

Base = declarative_base()
engine = db.create_engine("sqlite:///telegram.db")

session = sessionmaker()
session.configure(bind=engine)
my_session = session()


class Users(Base):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    telegram_id = db.Column(db.Integer)
    name = db.Column(db.String())
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)

    def isUserAdmin(self) -> bool:
        """:return true if the current user is admin"""
        return self.is_admin == True

    def isUserActive(self):
        return True if self.is_active else False

    def __repr__(self):
        return str(self.id)


class MasersAPI(Base):
    __tablename__ = "masterapi"
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer)
    api = db.Column(db.String())
    is_active = db.Column(db.Integer, default=True)

    def GetActiveMasters(self):
        return 'query all enabled masters'

    def __repr__(self):
        return str(self.id)


class Slaves(Base):
    __tablename__ = "slaves"
    id = db.Column(db.Integer, primary_key=True)
    parent = db.Column(db.Integer)
    slave = db.Column(db.String())
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return str(self.id)


def LoadSlaves(master_id):
    slaves = my_session.query(Slaves).filter(Slaves.parent == master_id).all()
    session.close_all()
    return [slave for slave in slaves]


def LoadUserIDByTelegramID(telegram_id):
    user_id = my_session.query(Users).filter(Users.telegram_id == telegram_id).first()
    print(user_id)
    return user_id.id


def ChangeMasterStatus(master_id, status):
    master_key = my_session.query(MasersAPI).filter(MasersAPI.id == master_id).first()
    master_key.is_active = status
    my_session.commit()
    return True


def LoadMasterKey(master_id):
    return my_session.query(MasersAPI).filter(MasersAPI.id == master_id).first().api


def DeleteMaster(master_id):
    master_key = my_session.query(MasersAPI).filter(MasersAPI.id == master_id).first()
    my_session.delete(master_key)
    my_session.commit()
    return True


def LoadMasters(user_id):
    masters = my_session.query(MasersAPI).where(MasersAPI.owner == user_id).all()
    print(masters)
    return masters


def IsUserAuthorized(user_id):
    user = my_session.query(Users).filter(Users.id == user_id).first()
    if user and bool(user.is_active):
        return True
    else:
        return False


def StoreMasterKey(**kwargs):
    api = kwargs.get('api')
    owner = kwargs.get('owner')
    my_session.add(MasersAPI(api=api, owner=owner))
    my_session.commit()


if __name__ == '__main__':
    pass
