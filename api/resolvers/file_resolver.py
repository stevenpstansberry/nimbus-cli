from models.file import File
from models import db_session

class FileResolver:
    @staticmethod
    def add_file(name, size, tags, s3_key):
        new_file = File(name=name, size=size, tags=tags, s3_key=s3_key)
        db_session.add(new_file)
        db_session.commit()
        return new_file

    @staticmethod
    def list_files():
        return db_session.query(File).all()
