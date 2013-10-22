import logging
import traceback
from webapp.models.database import db_session


class ModelsBase:
    def __init__(self, dt):
        for k, v in dt.items():
            setattr(self, k, v)


class ModelManager:

    def __init__(self):
        pass

    def insert(self, dt):
        try:
            class_f = self.get_model()
            m = class_f(dt)
            db_session.add(m)
            db_session.commit()
            return m
        except:
            logging.error(traceback.format_exc())
            return False

    def select_one(self, dt, key='id'):
        try:
            class_f = self.get_model()
            f = key + '=' + str(dt)
            ret = db_session.query(class_f).filter(f).first()
            return ret
        except:
            logging.error(traceback.format_exc())
            return False

    def select(self, where=True, order_by='id', offset=0, limit=20):
        try:
            class_f = self.get_model()
            ret = db_session.query(class_f).filter(where).order_by(order_by)[offset:limit]
            return ret
        except:
            logging.error(traceback.format_exc())
        finally:
            db_session.commit()

    def select_count(self, where=True):
        try:
            class_f = self.get_model()
            return db_session.query(class_f).filter(where).count()
        except:
            logging.error(traceback.format_exc())
        finally:
            db_session.commit()

    def update(self, dt, where=True):
        try:
            class_f = self.get_model()
            ret = db_session.query(class_f).filter(where)
            if(ret.count <= 0):
                return False
            for v in ret:
                for k2, v2 in dt.items():
                    setattr(v, k2, v2)
            db_session.commit()
            return True
        except:
            logging.error(traceback.format_exc())
            return False

    def delete(self, where=True):
        if(where is True):
            return False
        try:
            class_f = self.get_model()
            ret = db_session.query(class_f).filter(where)
            if(ret.count <= 0):
                return False
            for v in ret:
                db_session.delete(v)
            db_session.commit()
        except:
            logging.error(traceback.format_exc())
            return False
