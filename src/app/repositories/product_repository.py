# file: src/app/repositories/product_repository.py
from src.app.repositories.base import BaseRepository
from src.app.models.product import Product

class ProductRepository(BaseRepository):
    model = Product
