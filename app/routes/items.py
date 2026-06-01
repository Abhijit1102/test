from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Item
from app.schemas import ItemCreate, ItemPatch, ItemResponse, PaginatedItems

router = APIRouter(prefix="/items", tags=["Items"])


def get_item_or_404(db: Session, item_id: int) -> Item:
    item = db.scalar(select(Item).where(Item.id == item_id))
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    return item


@router.post(
    "/",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_item(
    item: ItemCreate,
    db: Annotated[Session, Depends(get_db)],
):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/", response_model=PaginatedItems)
def get_items(
    db: Annotated[Session, Depends(get_db)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    sort_by: Annotated[str, Query(pattern=r"^(id|name|created_at)$")] = "id",
    order: Annotated[str, Query(pattern=r"^(asc|desc)$")] = "asc",
):
    order_col = getattr(Item, sort_by)
    if order == "desc":
        order_col = order_col.desc()

    total = db.scalar(select(func.count()).select_from(Item))
    items = db.scalars(
        select(Item).order_by(order_col).offset(skip).limit(limit)
    ).all()

    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(
    item_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    return get_item_or_404(db, item_id)


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int,
    payload: ItemCreate,
    db: Annotated[Session, Depends(get_db)],
):
    db_item = get_item_or_404(db, item_id)
    for key, value in payload.model_dump().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.patch("/{item_id}", response_model=ItemResponse)
def patch_item(
    item_id: int,
    payload: ItemPatch,
    db: Annotated[Session, Depends(get_db)],
):
    db_item = get_item_or_404(db, item_id)
    update_data = payload.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )
    for key, value in update_data.items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    db_item = get_item_or_404(db, item_id)
    db.delete(db_item)
    db.commit()
    return None