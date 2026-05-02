# Кладовщик который копается в БД


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from schemas.books import SBookAdd, SBookUpdate
from models.books import BookModel


class BooksRepository:

    # Добавление объекта в БД
    @classmethod
    async def add_one_book(cls, book: SBookAdd, session: AsyncSession) -> BookModel:
        book_dict = book.model_dump()

        new_book = BookModel(**book_dict)

        session.add(new_book)

        await session.commit()
        await session.refresh(new_book)

        return new_book


    # Получение объекта по его ID в БД
    @classmethod
    async def get_one_book(cls, book_id: int, session: AsyncSession) -> BookModel | None:
        return await session.get(BookModel, book_id)


    # Получение объектов с 0 по 10, либо с нужным срезом
    @classmethod
    async def get_from_to_book(cls, book_from: int, book_to: int, session: AsyncSession) -> list[BookModel]:
        limit = max(0, book_to - book_from)

        limit = min(limit, 100)

        query = (
            select(BookModel).order_by(desc(BookModel.id)).offset(book_from).limit(limit)
        )

        result = await session.execute(query)
        return result.scalars().all()


    # Поиск книги по названию
    @classmethod
    async def get_book_by_name(cls, book_name: str, session: AsyncSession) -> list[BookModel]:
        found_book = select(BookModel).where(BookModel.title.contains(book_name))

        result = await session.execute(found_book)

        return result.scalars().all()


    # Поиск книг по автору
    @classmethod
    async def get_book_by_author(cls, book_author: str, session: AsyncSession) -> list[BookModel]:
        found_book = select(BookModel).where(BookModel.author == book_author)

        result = await session.execute(found_book)

        return result.scalars().all()


    # Обновление данных объекта по его ID
    @classmethod
    async def update_book(cls, book_id: int, data: SBookUpdate, session: AsyncSession) -> BookModel | None:
        book_in_db = await session.get(BookModel, book_id)

        if not book_in_db:
            return None

        update_book = data.model_dump(exclude_unset=True)

        for key, value in update_book.items():
            setattr(book_in_db, key, value)

        await session.commit()
        await session.refresh(book_in_db)

        return book_in_db


    # Обновление данных объекта по его названию
    @classmethod
    async def update_book(cls, book_name: str, data: SBookUpdate, session: AsyncSession) -> BookModel | None:
        book_in_db = select(BookModel).where(BookModel.title == book_name)
        found_book = await session.execute(book_in_db)
        book = found_book.scalars().first()

        if not book:
            return None

        update_book = data.model_dump(exclude_unset=True)

        for key, value in update_book.items():
            setattr(book, key, value)

        await session.commit()
        await session.refresh(book)

        return book


    # Удаление объекта из БД
    @classmethod
    async def delete_book(cls, book_id: int, session: AsyncSession) -> BookModel | None:
        book_in_db = await session.get(BookModel, book_id)

        if not book_in_db:
            return None

        await session.delete(book_in_db)
        await session.commit()

        return book_in_db