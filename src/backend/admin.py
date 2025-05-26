import os
from fastapi import Request
import fastapi
from sqladmin import Admin, ModelView
from backend.models import Product
from backend.database import engine
import base64
import secrets

VALID_USERNAME = os.getenv("VALID_USERNAME", "admin")
VALID_PASSWORD = os.getenv("VALID_PASSWORD", "admin")

class ProductAdmin(ModelView, model=Product):
    column_list = [Product.id, Product.name, Product.price, Product.stock] # type: ignore

def setup_admin(app):

    # Middleware to handle basic authentication for admin routes
    @app.middleware("http")
    async def admin_auth_middleware(request: Request, call_next):
        # Only apply authentication to `/admin` routes
        if request.url.path.startswith("/admin"):
            # Check for Basic Authentication header
            auth = request.headers.get("Authorization")
        
            if not auth or not auth.startswith("Basic "):
                return fastapi.responses.Response(
                    status_code=401,
                    headers={"WWW-Authenticate": "Basic"},
                    content="Authentification required"
                )
            try:
                # Split the header to get the encoded credentials
                # `Basic <Base64(username:password)>`
                encoded_credentials = auth.split(" ")[1]
                decoded = base64.b64decode(encoded_credentials).decode("utf-8")
                username, password = decoded.split(":", 1)

                # Compare the provided credentials with the valid ones
                if not (secrets.compare_digest(username, VALID_USERNAME) and secrets.compare_digest(password, VALID_PASSWORD)):
                    raise ValueError("Invalid credentials")
            except Exception:
                return fastapi.responses.Response(
                    status_code=401, # Unauthorized
                    headers={"WWW-Authenticate": "Basic"},
                    content="Invalid credentials"
                )

        # If the request is not for admin routes, or if authentication is successful, proceed with the request
        return await call_next(request)

    admin = Admin(app, engine)
    admin.add_view(ProductAdmin)
