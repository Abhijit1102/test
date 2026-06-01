from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ItemBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=2000)


class ItemCreate(ItemBase):
    tag_ids: Optional[list[int]] = Field(default=None, max_length=10)


class BulkItemCreate(BaseModel):
    items: list[ItemCreate] = Field(min_length=1, max_length=100)


class ItemPatch(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=2000)
    tag_ids: Optional[list[int]] = Field(default=None, max_length=10)


class TagResponse(BaseModel):
    id: int
    name: str


class ItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    tags: list[TagResponse] = []
    created_at: datetime
    updated_at: Optional[datetime]


class PaginatedItems(BaseModel):
    items: list[ItemResponse]
    total: int
    skip: int
    limit: int


class StatsResponse(BaseModel):
    total: int
    created_today: int
    updated_today: int
    deleted_today: int