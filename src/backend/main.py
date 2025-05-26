from fastapi import FastAPI, HTTPException, Path, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from backend.models import Product, ProductCreate
from sqlmodel import select, Session
from backend.database import get_session, init_db
from contextlib import asynccontextmanager
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

app = FastAPI(title="Fake-Zertifikatshop API",
    lifespan=lifespan # type: ignore
)
# Middleware to handle CORS (Cross-Origin Resource Sharing)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
 )
# Allow all origins for simplicity; adjust as needed

# API routes for managing products
@app.get("/api/products/", response_model=List[Product])
def get_products(session: Session = Depends(get_session)):
    """
    Retrieve a list of all products.
    """
    products = session.exec(select(Product)).all()
    return products

# Retrieve a single product by its ID
@app.get("/api/products/{product_id}", response_model=Product)
@app.get("/api/products/{product_id}/", response_model=Product)
def get_product(product_id: int, session: Session = Depends(get_session)):
    """
    Retrieve a product by its ID.
    """
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produkt nicht gefunden.")
    return product

# Create a new product
@app.post("/api/products/create/", response_model=Product)
def create_product(new_product: ProductCreate, session: Session = Depends(get_session)):
    product = Product.model_validate(new_product)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

# Update an existing product by its ID
@app.put("/api/products/{product_id}", response_model=Product)
@app.put("/api/products/{product_id}/", response_model=Product)
def update_product(
    product_id: int,
    updated_product: ProductCreate,
    session: Session = Depends(get_session)
):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produkt nicht gefunden.")
    
    for key, value in updated_product.dict(exclude_unset=True).items():
        setattr(product, key, value)
    
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

# Delete a product by its ID
@app.delete("/api/products/{product_id}")
@app.delete("/api/products/{product_id}/")
def delete_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produkt nicht gefunden.")
    session.delete(product)
    session.commit()
    return {"detail": f"Produkt mit ID {product_id} gelöscht."}