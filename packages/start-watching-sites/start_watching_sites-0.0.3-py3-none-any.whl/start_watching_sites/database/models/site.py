from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import pytz

Base = declarative_base()


class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, unique=True)
    status = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.timezone("Asia/Bangkok")))
    updated_at = Column(DateTime, onupdate=lambda: datetime.now(pytz.timezone("Asia/Bangkok")))
