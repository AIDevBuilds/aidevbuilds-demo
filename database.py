import bcrypt
from uuid import uuid4
from datetime import datetime

from models import UserInDB, Task, Priority


def _hash(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


users_db: dict[str, UserInDB] = {
    "admin": UserInDB(username="admin", hashed_password=_hash("password123")),
    "dev": UserInDB(username="dev", hashed_password=_hash("devpass")),
}

tasks_db: dict[str, Task] = {}


def _seed_tasks() -> None:
    samples = [
        Task(
            id=uuid4(),
            title="Set up CI/CD pipeline",
            description="Configure GitHub Actions for automated testing and deployment",
            priority=Priority.high,
            created_at=datetime.utcnow(),
            owner_username="admin",
        ),
        Task(
            id=uuid4(),
            title="Write API documentation",
            description="Document all endpoints with examples using OpenAPI",
            priority=Priority.medium,
            created_at=datetime.utcnow(),
            owner_username="admin",
        ),
        Task(
            id=uuid4(),
            title="Refactor auth module",
            description="Clean up token validation and improve error messages",
            priority=Priority.low,
            created_at=datetime.utcnow(),
            owner_username="dev",
        ),
    ]
    for task in samples:
        tasks_db[str(task.id)] = task


_seed_tasks()
