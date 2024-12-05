from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL database URL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://phuc:phuc@localhost:3300/document_store"

# Create the engine for connecting to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# SessionLocal class that will be used to create individual sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
