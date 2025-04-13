import logging

from database import database, user_table
from models.user import UserIn
from security import get_user

from fastapi import APIRouter, HTTPException, status

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/register", status_code=201)
async def register(user: UserIn):
    if await get_user(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with that email already exists",
        )
    data = user.model_dump()
    #hash password before storing in database
    query = user_table.insert().values(**data)
    logger.debug(query)
    await database.execute(query)
    return {"detail": "User created."}
