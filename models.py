from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Effect(Base):
    __tablename__ = "effects"
    __table_args__ = {"schema": "public"}

    effect_id = Column(Integer, primary_key=True)
    effect = Column(String,nullable=False, unique=True)

    cards = relationship("Card", back_populates="effect")


class Card(Base):
    __tablename__ = 'cards'
    __table_args__ = {"schema": "public"}

    card_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    keyword = Column(String, nullable=False)
    cost = Column(Integer, nullable=False)
    effect_id = Column(Integer, ForeignKey("public.effects.effect_id"), nullable=False)

    explanation = relationship("Explanation", back_populates="card")
    effect = relationship("Effect", back_populates="cards")
    card_qs = relationship("Card_q", back_populates="card")


class Question(Base):
    __tablename__ = 'questions'
    __table_args__ = {"schema": "public"}


    question_id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)

    card_qs = relationship("Card_q", back_populates="q")


class Card_q(Base):
    __tablename__ = "cards_q"
    __table_args__ = {"schema": "public"}

    card_id = Column(Integer, ForeignKey("public.cards.card_id"), primary_key=True)
    question_id = Column(Integer, ForeignKey("public.questions.question_id"), primary_key=True)

    q = relationship("Question", back_populates="card_qs")
    card = relationship("Card", back_populates="card_qs")


class Explanation(Base):
    __tablename__ = "explanations"
    __table_args__ = {"schema": "public"}

    card_id = Column(Integer, ForeignKey("public.cards.card_id"), primary_key=True)
    explanation = Column(String, nullable=False)

    card = relationship("Card", back_populates="explanation")
