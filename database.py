# Настройка движка (Engine) и сессий


from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from typing import Annotated
from fastapi import Depends


#Создали url чтобы поместить его в engine
db_url = "sqlite+aiosqlite:///library.db"

#Двигатель с помощью которого будет работать БД
engine = create_async_engine(db_url)

#Создатель сессии
new_session = async_sessionmaker(engine, expire_on_commit=False)


class BooksModel(DeclarativeBase, MappedAsDataclass):
    pass


async def get_db():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_db)]