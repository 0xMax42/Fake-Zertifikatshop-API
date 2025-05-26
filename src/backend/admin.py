import os
from fastapi import Request
import fastapi
from sqladmin import Admin, ModelView
from backend.models import Product, Stock
from backend.database import engine
import base64
import secrets

VALID_USERNAME = os.getenv("VALID_USERNAME", "admin")
VALID_PASSWORD = os.getenv("VALID_PASSWORD", "admin")

class ProductAdmin(ModelView, model=Product):
    """
    Admin interface for Product model.
    """
    column_list = [Product.id, Product.name, Product.price] # type: ignore

class StockAdmin(ModelView, model=Stock):
    """
    Admin interface for Stock model.
    """
    column_list = [Stock.id, Stock.quantity, Stock.product_id] # type: ignore

def setup_admin(app):
    # Middleware to handle basic authentication for admin routes
    @app.middleware("http")
    async def admin_auth_middleware(request: Request, call_next):
        if request.url.path.startswith("/admin"):
            auth = request.headers.get("Authorization")
            if not auth or not auth.startswith("Basic "):
                return fastapi.responses.Response(
                    status_code=401,
                    headers={"WWW-Authenticate": "Basic"},
                    content="Authentification required"
                )
            try:
                encoded_credentials = auth.split(" ")[1]
                decoded = base64.b64decode(encoded_credentials).decode("utf-8")
                username, password = decoded.split(":", 1)
                if not (secrets.compare_digest(username, VALID_USERNAME) and secrets.compare_digest(password, VALID_PASSWORD)):
                    raise ValueError("Invalid credentials")
            except Exception:
                return fastapi.responses.Response(
                    status_code=401,
                    headers={"WWW-Authenticate": "Basic"},
                    content="Invalid credentials"
                )

        return await call_next(request)

    admin = Admin(app, engine)
    admin.add_view(ProductAdmin)
    admin.add_view(StockAdmin)
