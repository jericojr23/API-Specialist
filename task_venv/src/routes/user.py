from fastapi import HTTPException, status, APIRouter
from models.user import UserCreate, User
from controllers.user import create_user, get_all_users, user_exists
from typing import List

user_router = APIRouter(prefix="/v1/users")


@user_router.get(
    "/view", response_model=List[User], response_description="List of all users"
)
def view_users():
    # Gets all the users
    try:
        users = get_all_users()
        return users
    except HTTPException as e:
        raise e


@user_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_description="Creation of user",
)
async def create_user_endpoint(user: UserCreate):
    try:
        # Check if user already exists
        if user_exists(user):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User already exists"
            )
        # Create a new user if they don't exist
        new_user = create_user(user)
        return new_user

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(detail=str(e))
