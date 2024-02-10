from fastapi import HTTPException, Depends

from src.api.user.service import UserService


def get_user(user_id: int, user_service: UserService = Depends()):
    print("came here.....")
    user = user_service.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
