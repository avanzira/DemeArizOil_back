# file: src/app/repositories/customer_repository.py
from app.repositories.base import BaseRepository
from app.models.customer import Customer

class CustomerRepository(BaseRepository):
    model = Customer
