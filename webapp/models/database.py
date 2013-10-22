from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config

engine = create_engine(config.get_app_conf(config.MODE)['DSN'], convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import webapp.models
    Base.metadata.create_all(bind=engine)

def clear_db():
    import webapp.models
    Base.metadata.drop_all(bind=engine)
