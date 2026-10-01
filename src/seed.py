import json
from pathlib import Path

from sqlmodel import Session, select

from src.models import Item


BASE_DIR = Path(__file__).resolve().parent.parent
SEED_FILE = BASE_DIR / "seed.json"


def load_seed_data(session: Session):

    existing_item = session.exec(select(Item)).first()

    if existing_item is not None:
        return

    with open(SEED_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    for item_data in data["items"]:
        item = Item(**item_data)
        session.add(item)

    session.commit()