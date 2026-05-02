#Запуск приложения, подключение роутеров и т.д.


from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import engine, BooksModel
from routers.books import router as BooksRouter


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(BooksModel.metadata.create_all)
    print("База данных запущена")
    yield
    print("База данных выключена")

app = FastAPI(lifespan=lifespan)
app.include_router(BooksRouter)
