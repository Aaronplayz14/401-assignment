from typing import Optional

from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class Item(SQLModel, table=True):
    id: str = Field(default=None, primary_key=True)

    title: str
    source: dict = Field(sa_column=Column(JSON))
    publishedAt: str
    url: str
    summary: str
    tags: list[str] = Field(sa_column=Column(JSON))
    position: int = Field(default=0, index=True)