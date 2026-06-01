from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import asc, desc, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_db
from app.models import Item
from app.schemas import ItemCreate, ItemPatch, ItemResponse, PaginatedItems

router = APIRouter(prefix="/items", tags=["Items"])


class ItemService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_404(self, item_id: int) -> Item:
        item = await self.db.scalar(select(Item).where(Item.id == item_id))
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id {item_id} not found",
            )
        return item

    async def create(self, data: ItemCreate) -> Item:
        db_item = Item(**data.model_dump())
        self.db.add(db_item)
        try:
            await self.db.commit()
            await self.db.refresh(db_item)
            return db_item
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Item with this name already exists",
            )

    async def list(
        self,
        skip: int,
        limit: int,
        sort_by: str,
        order: str,
        search: str | None,
    ) -> tuple[Sequence[Item], int]:
        stmt = select(Item)

        if search:
            stmt = stmt.where(Item.name.ilike(f"%{search}%"))

        total = await self.db.scalar(
            select(func.count()).select_from(stmt.subquery())
        )

        order_col = getattr(Item, sort_by)
        stmt = stmt.order_by(desc(order_col) if order == "desc" else asc(order_col))
        stmt = stmt.offset(skip).limit(limit)

        items = (await self.db.scalars(stmt)).all()
        return items, total

    async def update(self, item_id: int, data: ItemCreate) -> Item:
        db_item = await self.get_or_404(item_id)
        for key, value in data.model_dump().items():
            setattr(db_item, key, value)
        try:
            await self.db.commit()
            await self.db.refresh(db_item)
            return db_item
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Item with this name already exists",
            )

    async def patch(self, item_id: int, data: ItemPatch) -> Item:
        db_item = await self.get_or_404(item_id)
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields provided for update",
            )
        for key, value in update_data.items():
            setattr(db_item, key, value)
        try:
            await self.db.commit()
            await self.db.refresh(db_item)
            return db_item
        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Item with this name already exists",
            )

    async def delete(self, item_id: int) -> None:
        db_item = await self.get_or_404(item_id)
        await self.db.delete(db_item)
        await self.db.commit()


async def get_item_service(
    db: Annotated[AsyncSession, Depends(get_async_db)],
) -> ItemService:
    return ItemService(db)


ServiceDep = Annotated[ItemService, Depends(get_item_service)]


@router.post(
    "/",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new item",
)
async def create_item(
    item: ItemCreate,
    service: ServiceDep,
):
    return await service.create(item)


@router.get(
    "/",
    response_model=PaginatedItems,
    summary="List items with pagination",
)
async def get_items(
    service: ServiceDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    sort_by: Annotated[str, Query(pattern=r"^(id|name|created_at)$")] = "id",
    order: Annotated[str, Query(pattern=r"^(asc|desc)$")] = "asc",
    search: Annotated[str | None, Query(min_length=1, max_length=100)] = None,
):
    items, total = await service.list(skip, limit, sort_by, order, search)
    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit,
    }


@router.get(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Get a single item",
)
async def get_item(
    item_id: int,
    service: ServiceDep,
):
    return await service.get_or_404(item_id)


@router.put(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Full item update",
)
async def update_item(
    item_id: int,
    payload: ItemCreate,
    service: ServiceDep,
):
    return await service.update(item_id, payload)


@router.patch(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Partial item update",
)
async def patch_item(
    item_id: int,
    payload: ItemPatch,
    service: ServiceDep,
):
    return await service.patch(item_id, payload)


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an item",
)
async def delete_item(
    item_id: int,
    service: ServiceDep,
):
    await service.delete(item_id)
    return None