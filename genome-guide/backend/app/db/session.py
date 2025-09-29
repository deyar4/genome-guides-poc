from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define the location of the SQLite database file
SQLALCHEMY_DATABASE_URL = "sqlite:///./genome_guides.db"

# Create the SQLAlchemy engine
# connect_args is needed only for SQLite to allow multithreading
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class, which will be our actual database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# We can also create a Base class here for our models to inherit from
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()