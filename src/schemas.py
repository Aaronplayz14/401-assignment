from typing import List, Literal, Optional

from pydantic import BaseModel, StrictStr, ConfigDict


class SourceInput(BaseModel):
    name: StrictStr

    model_config = ConfigDict(extra="forbid")


class ItemCreate(BaseModel):
    title: StrictStr
    source: SourceInput
    publishedAt: StrictStr
    url: StrictStr
    summary: StrictStr
    tags: List[StrictStr]

    model_config = ConfigDict(extra="forbid")


class ItemUpdate(BaseModel):
    title: Optional[StrictStr] = None
    source: Optional[SourceInput] = None
    publishedAt: Optional[StrictStr] = None
    url: Optional[StrictStr] = None
    summary: Optional[StrictStr] = None
    tags: Optional[List[StrictStr]] = None

    model_config = ConfigDict(extra="forbid")


class ItemResponse(BaseModel):
    id: str
    title: str
    source: SourceInput
    publishedAt: str
    url: str
    summary: str
    tags: List[str]


class ItemListResponse(BaseModel):
    status: Literal["ok"] = "ok"
    data: List[ItemResponse]


class ItemSingleResponse(BaseModel):
    status: Literal["ok"] = "ok"
    data: ItemResponse


class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    status: Literal["error"] = "error"
    error: ErrorDetail