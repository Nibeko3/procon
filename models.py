from sqlalchemy import Column, Integer, String, ForeignKey,PrimaryKeyConstraint,DateTime
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

    id = Column(Integer, primary_key=True, index=True)
    current_turn = Column(Integer, default=1, nullable=False)
    current_player_id = Column(Integer, ForeignKey("players.user_id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    current_player = relationship("Player", foreign_keys=[current_player_id])
    players = relationship("MatchPlayer", back_populates="match")

class MatchPlayer(Base):
    __tablename__ = "match_players"
    __table_args__ = (
        # 複合主キー
        PrimaryKeyConstraint("match_id", "my_id"),
    )

    match_id = Column(Integer, ForeignKey("matches.id"))
    my_id = Column(Integer, ForeignKey("players.user_id"))
    opponent_id = Column(Integer, ForeignKey("players.user_id"))

    wallet = Column(Integer, default=100, nullable=False)
    production_power = Column(Integer, default=200, nullable=False)

    match = relationship("Match", back_populates="players")
    my_player = relationship("Player", foreign_keys=[my_id], backref="my_match_entries")
    opponent_player = relationship("Player", foreign_keys=[opponent_id], backref="opponent_match_entries")
