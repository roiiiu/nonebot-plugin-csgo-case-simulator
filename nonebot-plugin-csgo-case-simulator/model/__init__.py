from typing import List, Optional
from pydantic import BaseModel


class Contains(BaseModel):
    id: str
    name: str
    rarity: str


class Crate(BaseModel):
    id: str
    name: str
    description: Optional[str]
    type: str
    first_sale_date: Optional[str]
    contains: List[Contains]
    contains_rare: List[Contains]
    image: str


class Skin(BaseModel):
    id: str
    name: str
    description: Optional[str]
    weapon: Optional[str]
    category: str
    pattern: Optional[str]
    min_float: Optional[float]
    max_float: Optional[float]
    rarity: str
    stattrak: bool
    paint_index: Optional[str]
    image: str


class SelectedSkin(BaseModel):
    id: str
    name: str
    image: str
    rarity: str
    wear_rating: Optional[float]
