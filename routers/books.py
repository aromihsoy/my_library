from fastapi import APIRouter, Query, HTTPException, status
from typing import Annotated
from schemas.books import SBook, SBookAdd, SBookUpdate
from database import SessionDep
from repository import BooksRepository


router = APIRouter(
    prefix = "/books",
    tags=["books"],
)


# Добавление объекта в БД
@router.post("", response_model=SBook)
async def add_one_book(book: SBookAdd, session: SessionDep):
    created_book = await BooksRepository.add_one_book(book, session)

    return created_book


# Получение объекта по его ID в БД
@router.get("/{book_id}")
async def get_one_book(book_id: int, session: SessionDep):
    book = await BooksRepository.get_one_book(book_id, session)
    return book


# Получение объектов с 0 по 10, либо с нужным срезом
@router.get("")
async def get_from_to_book(
        session: SessionDep,
        book_from: Annotated[int, Query(ge=0)] = 0,
        book_to: Annotated[int, Query(le=100)] = 10
):
    books = await BooksRepository.get_from_to_book(book_from, book_to, session)
    return books


# Поиск книги по названию
@router.get("/name/{book_name}")
async def get_book_by_name(book_name: str, session: SessionDep):
    return await BooksRepository.get_book_by_name(book_name, session)


# Поиск книг по автору
@router.get("/author/{book_author}")
async def get_book_by_author(book_author: str, session: SessionDep):
    return await BooksRepository.get_book_by_author(book_author, session)


# Обновление данных объекта по его ID
@router.put("/{book_id}")
async def update_book(book_id: int, book: SBookUpdate, session: SessionDep):
    query = await BooksRepository.update_book(book_id, book, session)

    if not query:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Книга не найдена"
        )

    return {f"Книга с ID: {book_id} была изменена/обновлена"}


# Обновление данных объекта по его названию
@router.put("/update/{book_name}")
async def update_book(book_name: str, book: SBookUpdate, session: SessionDep):
    query = await BooksRepository.update_book(book_name, book, session)

    if not query:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Книга не найдена"
        )

    return {f"Книга с названием: {book_name} была изменена/обновлена"}


# Удаление объекта из БД
@router.delete("/{book_id}")
async def delete_book(book_id: int, session: SessionDep):
    task = await BooksRepository.delete_book(book_id, session)

    if not task:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Книга не найдена, удалять нечего"
        )

    return {
        "message": "Книга успешно удалена",

        "deleted_book": task
    }