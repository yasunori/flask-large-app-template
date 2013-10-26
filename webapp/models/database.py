from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config

conf = config.get_app_conf(config.MODE)['DB']
engine = create_engine(conf['DSN'], convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=conf['AUTO_COMMIT'],
                                         autoflush=conf['AUTO_FLUSH'],
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import webapp.models
    Base.metadata.create_all(bind=engine)

def clear_db():
    import webapp.models
    Base.metadata.drop_all(bind=engine)
