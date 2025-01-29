from sqlalchemy import Column, Integer, String, DateTime
from . import Base
from datetime import datetime, timezone

class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)           
    size = Column(Integer, nullable=False)          
    tags = Column(String)                           
    upload_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))  
    s3_key = Column(String, nullable=False)