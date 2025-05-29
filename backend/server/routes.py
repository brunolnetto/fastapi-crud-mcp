from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.server.models import ItemCreate, ItemUpdate, ItemOut
from backend.server.db import get_db
import backend.server.crud as crud
from backend.server.logger import logger
from backend.server.models import PaginationParams

router = APIRouter()

# ─── CRUD Endpoints ─────────────────────────────────────────────────────────────

@router.post(
    "/items/",
    response_model=ItemOut,
    summary="Create a new item",
    description="Create a new item with the provided name and description.",
    tags=["items"],
    operation_id="create_item"
)
def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
):
    logger.info(f"Creating item: {item.name}")
    return crud.create_item(db, item)


@router.get(
    "/items/",
    response_model=list[ItemOut],
    summary="Retrieve all items",
    description="Retrieve a list of all items, with optional pagination.",
    tags=["items"],
    operation_id="get_all_items"
)
def get_all_items(
    params: PaginationParams = Depends(),
    db: Session = Depends(get_db),
):
    logger.info(f"Getting items")
    return crud.get_items(db, skip=params.skip, limit=params.limit)


@router.get(
    "/items/{item_id}",
    response_model=ItemOut,
    summary="Retrieve a single item",
    description="Retrieve the item with the given ID.",
    tags=["items"],
    operation_id="get_item"
)
def get_user_info(
    item_id: int,
    db: Session = Depends(get_db),
):
    item = crud.get_item(db, item_id)

    logger.info(f"Getting item information: {item}")

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put(
    "/items/{item_id}",
    response_model=ItemOut,
    summary="Update an existing item",
    description="Update the item with the given ID using the provided data.",
    tags=["items"],
    operation_id="update_item"
)
def update_user_info(
    item_id: int,
    item: ItemUpdate,
    db: Session = Depends(get_db),
):
    updated = crud.update_item(db, item_id, item)

    logger.info(f"Updated item information: {updated}")

    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated


@router.delete(
    "/items/{item_id}",
    summary="Delete an item",
    description="Delete the item with the given ID.",
    tags=["items"],
    operation_id="delete_item"
)
def delete_user_info(
    item_id: int,
    db: Session = Depends(get_db),
):
    deleted = crud.delete_item(db, item_id)

    logger.info(f"Deleted item information: {deleted}")
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"ok": True}
