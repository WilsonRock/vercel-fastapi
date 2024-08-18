# models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class NotificationReceived(Base):
    __tablename__ = 'notification_received'
    id = Column(Integer, primary_key=True, index=True)
    notification_id = Column(String, index=True)
    title = Column(String)
    message = Column(String)
    user_id = Column(String)

class NotificationOpened(Base):
    __tablename__ = 'notification_opened'
    id = Column(Integer, primary_key=True, index=True)
    notification_id = Column(String, index=True)
    user_id = Column(String)

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
