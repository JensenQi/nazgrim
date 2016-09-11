from config import DATABASE_URI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DATABASE_URI)
DBSession = sessionmaker(engine)

