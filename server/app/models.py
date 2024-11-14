from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Palavra(Base):
    __tablename__ = 'WORDLIST'
    id: Mapped[str] = mapped_column(primary_key=True)
    palavra: Mapped[str] = mapped_column(String)
    dica: Mapped[str] = mapped_column(String)
    acertos: Mapped[int] = mapped_column(Integer)
    erros: Mapped[int] = mapped_column(Integer)
    used: Mapped[int] = mapped_column(Integer)
    ativa: Mapped[int] = mapped_column(Boolean)


class CurrentDay(Base):
    __tablename__ = 'curDay'
    curDay: Mapped[int] = mapped_column(Integer, primary_key=True)


class UsedCount(Base):
    __tablename__ = 'usedCount'
    usedCount: Mapped[int] = mapped_column(Integer, primary_key=True)


class Data:
    # def __init__(self):
    palavra: str
    dica: str
    curDay: int

    def to_dict(self):
        return vars(self)