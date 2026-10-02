from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import Response
from sqlmodel import Session, select

from src.database import get_session
from src.models import Item
from src.schemas import (
    ItemCreate,
    ItemListResponse,
    ItemResponse,
    ItemSingleResponse,
    ItemUpdate
)
from src.validation import validate_item_values


router = APIRouter(
    prefix="/api/v1/items",
    tags=["items"]
)


def serialize_item(item: Item) -> ItemResponse:

    return ItemResponse(
        id=item.id,
        title=item.title,
        source=item.source,
        publishedAt=item.publishedAt,
        url=item.url,
        summary=item.summary,
        tags=item.tags
    )


def get_next(session: Session) -> int:

    last_item = session.exec(select(Item).order_by(Item.position.desc())).first()

    if last_item is None:
        return 0

    return last_item.position + 1


def validation_error(message: str):
    raise HTTPException(
        status_code=400,
        detail={
            "code": "VALIDATION_ERROR",
            "message": message
        }
    )


@router.get("", response_model=ItemListResponse)
def get_items(limit: int = Query(default=10, ge=1, le=50), offset: int = Query(default=0,ge=0), session: Session = Depends(get_session)):
    statement = (select(Item).order_by(Item.position).offset(offset).limit(limit))

    items = session.exec(statement).all()

    return ItemListResponse(status="ok", data=[serialize_item(item) for item in items])


@router.get("/{item_id}", response_model=ItemSingleResponse)
def get_item(item_id: str, session: Session = Depends(get_session)):

    item = session.get(Item, item_id)
    if item is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "NOT_FOUND",
                "message": "Item not found"
            }
        )

    return ItemSingleResponse(status="ok",data=serialize_item(item))


@router.post(
    "",
    response_model=ItemSingleResponse,
    status_code=201,
)
def create_item(payload: ItemCreate, session: Session = Depends(get_session)):
    data = payload.model_dump()

    try:
        validate_item_values(data)
    except ValueError as error:
        validation_error(str(error))

    item = Item(
        id=str(uuid4()),
        position=get_next(session),
        title=payload.title,
        source=payload.source.model_dump(),
        publishedAt=payload.publishedAt,
        url=payload.url,
        summary=payload.summary,
        tags=list(payload.tags)
    )

    session.add(item)
    session.commit()
    session.refresh(item)

    return ItemSingleResponse(status="ok", data=serialize_item(item))


@router.patch("/{item_id}",response_model=ItemSingleResponse)
def update_item(item_id: str, payload: ItemUpdate, session: Session = Depends(get_session)):

    item = session.get(Item, item_id)

    if item is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "NOT_FOUND",
                "message": "Item not found"
            }
        )

    data = payload.model_dump(exclude_unset=True)

    for field_name, value in data.items():
        if value is None:
            validation_error(f"{field_name} must not be null")

    try:
        validate_item_values(data)
    except ValueError as error:
        validation_error(str(error))

    if "title" in data:
        item.title = payload.title

    if "source" in data:
        item.source = payload.source.model_dump()

    if "publishedAt" in data:
        item.publishedAt = payload.publishedAt

    if "url" in data:
        item.url = payload.url

    if "summary" in data:
        item.summary = payload.summary

    if "tags" in data:
        item.tags = list(payload.tags)

    session.add(item)
    session.commit()
    session.refresh(item)

    return ItemSingleResponse(status="ok", data=serialize_item(item))


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: str, session: Session = Depends(get_session)):

    item = session.get(Item, item_id)

    if item is None:
        raise HTTPException(
            status_code=404,
            detail={
                "code": "NOT_FOUND",
                "message": "Item not found"
            }
        )

    session.delete(item)
    session.commit()

    return Response(status_code=204)