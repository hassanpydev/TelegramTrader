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