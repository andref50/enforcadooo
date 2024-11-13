from sqlalchemy import String, Integer, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class Palavra(Base):
    __tablename__ = 'WORDLIST'
    id: Mapped[str] = mapped_column(primary_key=True)
    palavra: Mapped[str] = mapped_column(String)
    dica: Mapped[str] = mapped_column(String)

class CurrentDay(Base):
    __tablename__ = 'curDay'
    current_day: Mapped[int] = mapped_column(Integer, primary_key=True)