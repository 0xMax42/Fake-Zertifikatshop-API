from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .models import Product  # vermeidet zirkuläre Imports zur Laufzeit

class Stock(SQLModel, table=True):
    """
    Represents the stock information stored in a separate table.

    Attributes:
        id (Optional[int]): The primary key of the stock entry.
        quantity (int): The quantity of the product in stock.
        product_id (Optional[int]): The foreign key referencing the product.
        product (Optional[Product]): The associated product.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    quantity: int
    product_id: Optional[int] = Field(default=None, foreign_key="product.id")

    product: Optional["Product"] = Relationship(back_populates="stock")


class StockRead(BaseModel):
    """
    Pydantic response model for stock.

    Attributes:
        quantity (int): The quantity in stock.
    """
    quantity: int

    class Config:
        orm_mode = True


class ProductBase(SQLModel):
    """
    Base model for product information.

    Attributes:
        name (str): The name of the product.
        short_description (str): A brief description of the product.
        product_description (str): A detailed description of the product.
        price (float): The price of the product.
    """
    name: str
    short_description: str
    product_description: str
    price: float


class Product(SQLModel, table=True):
    """
    Represents a product entity in the SQLite database.

    Attributes:
        id (Optional[int]): The primary key of the product.
        stock (Optional[Stock]): The associated stock entry.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    short_description: str
    product_description: str
    price: float

    stock: Optional["Stock"] = Relationship(back_populates="product")


class ProductCreate(ProductBase):
    """
    Input model for creating a product.

    Attributes:
        stock (Stock): Stock data for the product.
    """
    stock: Stock


class ProductRead(ProductBase):
    """
    Response model for returning product data with stock.

    Attributes:
        id (int): The unique identifier of the product.
        stock (StockRead): The stock information.
    """
    id: int
    stock: Optional[StockRead]

    class Config: # type: ignore
        orm_mode = True
