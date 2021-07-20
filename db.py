from models import *


def LoadSlaves(master_id):
    slaves = my_session.query(Slaves).filter(Slaves.parent == master_id).all()
    session.close_all()
    return [slave for slave in slaves]


def LoadUserIDByTelegramID(telegram_id):
    user_id = my_session.query(Users).filter(Users.telegram_id == telegram_id).first()
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


def StoreSlave(master_id, slave):
    my_session.add(Slaves(parent=master_id, slave=slave))
    my_session.commit()


def StoreMasterKey(**kwargs):
    api = kwargs.get('api')
    owner = kwargs.get('owner')
    my_session.add(MasersAPI(api=api, owner=owner))
    my_session.commit()


if __name__ == '__main__':
    pass
