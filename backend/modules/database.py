from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules.models import Base

engine = create_engine('sqlite:///database.db', echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db_session = Session()
