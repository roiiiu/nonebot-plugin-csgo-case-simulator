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


class Weapon(BaseModel):
    id: str
    name: Optional[str]


class Category(BaseModel):
    id: str
    name: str


class Pattern(BaseModel):
    id: str
    name: str


class Rarity(BaseModel):
    id: str
    name: str


class Wear(BaseModel):
    id: str
    name: str


class Collections(BaseModel):
    id: str
    name: str
    image: str


class Crates(BaseModel):
    id: str
    name: str
    image: str


class Skin(BaseModel):
    id: str
    name: str
    description: Optional[str]
    weapon: Optional[Weapon]
    category: Category
    pattern: Optional[Pattern]
    min_float: Optional[float]
    max_float: Optional[float]
    rarity: Rarity
    stattrak: bool
    souvenir: Optional[bool]
    paint_index: Optional[str]
    wears: Optional[List[Wear]]
    collection: Optional[List[Collections]]
    crates: Optional[List[Crates]]
    image: str


class SelectedSkin(BaseModel):
    id: str
    name: str
    image: str
    rarity: str
    wear: Optional[str]
