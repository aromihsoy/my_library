# Схемы Pydantic для HTTP методов в роутере


from pydantic import BaseModel, ConfigDict, Field


class SBookBase(BaseModel):
    title: str
    author: str
    year: int
    pages: int = Field(gt = 10)
    is_read: bool = False


class SBookAdd(SBookBase):
    pass


class SBookUpdate(SBookBase):
    pass


class SBook(SBookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
