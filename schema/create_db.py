from sqlalchemy import create_engine, Column, BigInteger, String, TIMESTAMP
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the database URL from .env
DB_URL = os.getenv("DB_URL")

# Define the Base class for SQLAlchemy
Base = declarative_base()

# Define the ESIToken model
class ESIToken(Base):
    __tablename__ = "esi_tokens"

    discord_user_id = Column(BigInteger, primary_key=True)
    character_id = Column(BigInteger, primary_key=True)
    guild_id = Column(BigInteger)
    access_token = Column(String)
    refresh_token = Column(String)
    token_expiry = Column(TIMESTAMP)
    scopes = Column(String)

# Create the SQLAlchemy engine and connect to the DB
engine = create_engine(DB_URL)

# Create all tables defined in the Base
Base.metadata.create_all(engine)

print("Database and table created.")
