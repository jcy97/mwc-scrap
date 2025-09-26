from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from config import DATABASE_URL

Base = declarative_base()


class ExhibitionRule(Base):
    __tablename__ = "exhibition_rules"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), nullable=False)
    title = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    categories = relationship("RuleCategory", back_populates="exhibition_rule")


class RuleCategory(Base):
    __tablename__ = "rule_categories"

    id = Column(Integer, primary_key=True, index=True)
    exhibition_rule_id = Column(Integer, ForeignKey("exhibition_rules.id"))
    name = Column(String(200), nullable=False)
    name_en = Column(String(200))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    exhibition_rule = relationship("ExhibitionRule", back_populates="categories")
    rule_items = relationship("RuleItem", back_populates="category")


class RuleItem(Base):
    __tablename__ = "rule_items"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("rule_categories.id"))
    content_ko = Column(Text)
    content_en = Column(Text)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    category = relationship("RuleCategory", back_populates="rule_items")


def init_database():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    return engine


def get_session():
    engine = init_database()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()
