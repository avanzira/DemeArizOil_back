# file: src/app/repositories/user_repository.py
from app.repositories.base import BaseRepository
from app.models.user import User

class UserRepository(BaseRepository):
    model = User

    def get_by_username(self, username: str):
        return (
            self.db.query(User)
            .filter(User.username == username, User.is_active == True)
            .first()
        )

    def get_by_email(self, email: str):
        return (
            self.db.query(User)
            .filter(User.email == email, User.is_active == True)
            .first()
        )
