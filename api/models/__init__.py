# models/__init__.py
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Configure the database connection
engine = create_engine(DATABASE_URL, echo=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()


def init_db(flask_app):
    """Initialize the database and bind it to the Flask app."""
    Base.metadata.create_all(bind=engine)

    @flask_app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
