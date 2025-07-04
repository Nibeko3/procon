from sqlalchemy import Column, Integer, String, ForeignKey,DateTime
from sqlalchemy.sql import func
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

class Player(Base):
    __tablename__ = "players"
    __table_args__ = {"schema": "public"}

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    score = Column(Integer, default=1500)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 逆参照：参加したマッチ
    matches_as_player1 = relationship("Match", back_populates="player1", foreign_keys="Match.player1_id")
    matches_as_player2 = relationship("Match", back_populates="player2", foreign_keys="Match.player2_id")

class Match(Base):
    __tablename__ = "matches"
    __table_args__ = {"schema": "public"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    player1_id = Column(Integer, ForeignKey("public.players.user_id"), nullable=False)
    player2_id = Column(Integer, ForeignKey("public.players.user_id"), nullable=True)
    current_turn = Column(Integer, default=1, nullable=False)
    current_player_id = Column(Integer, ForeignKey("public.players.user_id"), nullable=False)

    wallet_player1 = Column(Integer, default=100, nullable=False)
    wallet_player2 = Column(Integer, default=100, nullable=False)
    production_power_player1 = Column(Integer, default=200, nullable=False)
    production_power_player2 = Column(Integer, default=200, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 参照
    player1 = relationship("Player", foreign_keys=[player1_id], back_populates="matches_as_player1")
    player2 = relationship("Player", foreign_keys=[player2_id], back_populates="matches_as_player2")
