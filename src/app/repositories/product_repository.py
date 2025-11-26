# file: src/app/repositories/product_repository.py
from app.repositories.base import BaseRepository
from app.models.product import Product

class ProductRepository(BaseRepository):
    model = Product
