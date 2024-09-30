from sqlalchemy import ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession


engine = create_async_engine(url='sqlite+aiosqlite:///user.db')


async_session = async_sessionmaker(engine, class_=AsyncSession)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id = mapped_column(BigInteger, nullable=True)
    tg_name: Mapped[str] = mapped_column(String(20), nullable=True)
    age: Mapped[str] = mapped_column(String(20), nullable=True)
    question2: Mapped[str] = mapped_column(String(128), nullable=True)
    question3: Mapped[str] = mapped_column(String(20), nullable=True)
    question4: Mapped[str] = mapped_column(String(20), nullable=True)
    question5: Mapped[str] = mapped_column(String(20), nullable=True)


async def async_mainm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



