"""DB utils and helpers."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from scoodent.common import config


Base = declarative_base()


__SESSION = None
"""Global session object."""


def get_engine(debug=None):
    """Return ORM engine."""

    debug = config.DEBUG if debug is None else debug
    return create_engine(config.DB_URI, echo=debug)


def get_session(debug=None):
    """Return DB session."""

    global __SESSION

    if not __SESSION:
        engine = get_engine(debug)
        Base.metadata.bind = engine
        __SESSION = sessionmaker(bind=engine)()

    return __SESSION


def insert_objects(obj, obj_id=None):
    """Insert object or objects to DB."""

    session = get_session()
    if isinstance(obj, (tuple, list)):
        session.add_all(obj)
    else:
        if obj_id is None:
            session.add(obj)
        else:
            # Updating object
            obj.id = obj_id
            session.merge(obj)

    session.commit()
