from app.domain.user.model import User
from app.domain.user.schema import RegisterRequest, LoginRequest
from app.repositories.user import user_repo
from app.core.exceptions import NotFound, Conflict, Unauthorized
from app.core.security import hash_password, verify_password

def register(data: RegisterRequest) -> User:
    exiting_user = user_repo.find_by_username(data.username)

    if exiting_user:
        raise Conflict("Username already registered!")

    user = User(id=user_repo.next_id(),
                username=data.username,
                password=hash_password(data.password),
                role = "user"
            )
    return user_repo.add(user)

def login(data: LoginRequest) -> User:
    user = user_repo.find_by_username(data.username)

    if not user:
        raise Unauthorized() 
    #check password
    if not verify_password(data.password, user.password):
        raise Unauthorized()
    return user

def get_user(user_id: int) -> User:
    user = user_repo.get(user_id)

    if not user:
        raise NotFound("User")

    return user