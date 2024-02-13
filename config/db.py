from sqlalchemy import create_engine,MetaData
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

import os 

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"))
Session = sessionmaker(bind=engine)

session = Session()