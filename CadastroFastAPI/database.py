from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Substitua pelos seus dados reais
DATABASE_URL = "postgresql://postgres:LZZpPLET6iCt5ZFZ@db.ymarbpmondxgajrfnccr.supabase.co:5432/postgres"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
