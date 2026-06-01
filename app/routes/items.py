from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Item
from app.schemas import ItemCreate, ItemResponse

router = APIRouter(prefix="/items", tags=["Items"])


@router.post("/", response_model=ItemResponse)
def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db)
):
    db_item = Item(
        name=item.name,
        description=item.description
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


@router.get("/", response_model=list[ItemResponse])
def get_items(
    db: Session = Depends(get_db)
):
    return db.query(Item).all()


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    item = (
        db.query(Item)
        .filter(Item.id == item_id)
        .first()
    )

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return item


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int,
    payload: ItemCreate,
    db: Session = Depends(get_db)
):
    db_item = (
        db.query(Item)
        .filter(Item.id == item_id)
        .first()
    )

    if not db_item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    db_item.name = payload.name
    db_item.description = payload.description

    db.commit()
    db.refresh(db_item)

    return db_item


@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    db_item = (
        db.query(Item)
        .filter(Item.id == item_id)
        .first()
    )

    if not db_item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    db.delete(db_item)
    db.commit()

    return {"message": "Deleted successfully"}