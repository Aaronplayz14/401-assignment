from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from src.database import get_session
from src.models import Item


router = APIRouter(
    prefix="/api/v1/items",
    tags=["items"],
)


@router.get("")
def get_items(session: Session = Depends(get_session)):
    items = session.exec(select(Item)).all()

    return items


@router.get("/{item_id}")
def get_item(item_id: int, session: Session = Depends(get_session)):
    item = session.get(Item, item_id)

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
        )

    return item