from fastapi import APIRouter, HTTPException, status
from models.user import UserCreate, User
from controllers.user_controller import create_user, get_all_users
from typing import List

router = APIRouter(prefix="/v1/users")


@router.get("/view", response_model=List[User])
def view_users():
    # Gets all the users
    try:
        users = get_all_users()
        return users
    except HTTPException as e:
        raise e


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(user: UserCreate):
    try:
        new_user = create_user(user)
        return new_user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
