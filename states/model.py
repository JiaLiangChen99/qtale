from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///music.db")

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# 建表

class Music(Base):
    __tablename__ = "music"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    image_path = Column(String)
    music_path = Column(String)

Base.metadata.create_all(bind=engine)
