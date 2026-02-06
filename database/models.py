from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# استخدام PostgreSQL من Railway
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///stock.db')
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
Base = declarative_base()

class Price(Base):
    __tablename__ = 'prices'
    symbol = Column(String(10), primary_key=True)
    date = Column(DateTime, primary_key=True)
    open = Column(Numeric(10, 4))
    high = Column(Numeric(10, 4))
    low = Column(Numeric(10, 4))
    close = Column(Numeric(10, 4))
    volume = Column(Integer)

class Analysis(Base):
    __tablename__ = 'analysis'
    symbol = Column(String(10), primary_key=True)
    date = Column(DateTime, primary_key=True)
    current_price = Column(Numeric(10, 4))
    trend = Column(String(50))
    signal = Column(String(20))
    score = Column(Integer)
    rsi = Column(Numeric(5, 2))
    sma_20 = Column(Numeric(10, 4))
    sma_50 = Column(Numeric(10, 4))
    target_1 = Column(Numeric(10, 4))
    target_2 = Column(Numeric(10, 4))
    stop_loss = Column(Numeric(10, 4))

def init_database():
    """تهيئة قاعدة البيانات - إنشاء الجداول"""
    Base.metadata.create_all(engine)
    print("✅ Database tables created")

def get_session():
    """الحصول على جلسة قاعدة البيانات"""
    Session = sessionmaker(bind=engine)
    return Session()
