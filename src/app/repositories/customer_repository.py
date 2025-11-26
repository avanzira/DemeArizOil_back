# file: src/app/repositories/customer_repository.py
from src.app.repositories.base import BaseRepository
from src.app.models.customer import Customer

class CustomerRepository(BaseRepository):
    model = Customer
