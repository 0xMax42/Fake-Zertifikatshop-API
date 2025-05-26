from sqlmodel import SQLModel, Field
from typing import Optional

class ProductBase(SQLModel):
    """
    Base model for product information.

    Attributes:
        name (str): The name of the product.
        short_description (str): A brief description of the product.
        product_description (str): A detailed description of the product.
        price (float): The price of the product.
        stock (Stock): The stock information of the product.
    """
    name: str
    short_description: str
    product_description: str
    price: float
    stock: int


class Product(ProductBase, table=True):
    """
    Represents a product entity in the SQLite database.

    Attributes:
        id (Optional[int]): The primary key of the product. Defaults to None.
    """
    id: Optional[int] = Field(default=None, primary_key=True)


class ProductCreate(ProductBase):
    """
    Input model for creating a product.

    Inherits all attributes from ProductBase.
    """
    pass
