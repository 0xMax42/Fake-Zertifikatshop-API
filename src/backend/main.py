from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from backend.admin import setup_admin
from backend.models import Product, ProductCreate, ProductRead, Stock
from sqlmodel import select, Session
from backend.database import get_session, init_db
from typing import List, AsyncGenerator

# Main application file for the Fake-Zertifikatshop API
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan event handler to initialize the database.
    This function is called when the application starts up and ensures that
    the database is initialized before handling any requests.
    """
    init_db()
    yield

app = FastAPI(title="Fake-Zertifikatshop API", lifespan=lifespan)  # type: ignore
setup_admin(app)

# Middleware to handle CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes for managing products
@app.get("/api/products/", response_model=List[ProductRead])
def get_products(session: Session = Depends(get_session)):
    """
    Retrieve a list of all products.
    """
    products = session.exec(select(Product)).all()
    return products

@app.get("/api/products/{product_id}", response_model=ProductRead)
@app.get("/api/products/{product_id}/", response_model=ProductRead)
def get_product(product_id: int, session: Session = Depends(get_session)):
    """
    Retrieve a product by its ID.
    """
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produkt nicht gefunden.")
    return product

@app.post("/api/products/create/", response_model=ProductRead)
def create_product(new_product: ProductCreate, session: Session = Depends(get_session)):
    """
    Create a new product and its associated stock entry.
    """
    product = Product(
        name=new_product.name,
        short_description=new_product.short_description,
        product_description=new_product.product_description,
        price=new_product.price,
    )
    session.add(product)
    session.flush()

    stock = Stock(quantity=new_product.stock.quantity, product_id=product.id)
    session.add(stock)

    session.commit()
    session.refresh(product)
    return product

@app.put("/api/products/{product_id}", response_model=ProductRead)
@app.put("/api/products/{product_id}/", response_model=ProductRead)
def update_product(
    product_id: int,
    updated_product: ProductCreate,
    session: Session = Depends(get_session)
):
    """
    Update an existing product and its stock.
    """
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produkt nicht gefunden.")

    for key, value in updated_product.dict(exclude_unset=True, exclude={"stock"}).items():
        setattr(product, key, value)

    if product.stock:
        product.stock.quantity = updated_product.stock.quantity
    else:
        stock = Stock(quantity=updated_product.stock.quantity, product_id=product.id)
        session.add(stock)

    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@app.delete("/api/products/{product_id}")
@app.delete("/api/products/{product_id}/")
def delete_product(product_id: int, session: Session = Depends(get_session)):
    """
    Delete a product and its associated stock entry.
    """
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produkt nicht gefunden.")

    if product.stock:
        session.delete(product.stock)

    session.delete(product)
    session.commit()
    return {"detail": f"Produkt mit ID {product_id} gelöscht."}