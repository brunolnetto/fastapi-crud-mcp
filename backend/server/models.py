from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

from reprlib import repr

Base = declarative_base()

# ─── Pydantic “Params” Models ─────────────────────────────────────────────────

# SQLAlchemy model
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    
    def __repr__(self):
        args=f"id={self.id}, name={self.name}, description={repr(self.description)}"
        return f"Item({args})"

# Pydantic schemas
class ItemBase(BaseModel):
    name: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    pass

class ItemOut(ItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class PaginationParams(BaseModel):
    skip: int = Field(0, ge=0, description="Number of items to skip")
    limit: int = Field(10, gt=0, le=100, description="Max number of items to return")