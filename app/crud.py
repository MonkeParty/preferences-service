from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from model import UserInfoDB
from pydantic import BaseModel
from typing import List, Optional

class UserInfo(BaseModel):
    user_id: int
    avg_rating: float
    genres_preference: dict
    tags_preference: dict
    svd_vector: List[float]

async def create_user_info(db: AsyncSession, user_info: UserInfo) -> UserInfoDB:
    db_user_info = UserInfoDB(**user_info.model_dump())
    db.add(db_user_info)
    await db.commit()
    await db.refresh(db_user_info)
    return db_user_info

async def get_user_info(db: AsyncSession, user_id: int) -> UserInfoDB:
    result = await db.execute(select(UserInfoDB).where(UserInfoDB.user_id == user_id))
    return result.scalars().first()

async def get_all_users(db: AsyncSession) -> List[UserInfoDB]:
    result = await db.execute(select(UserInfoDB))
    return result.scalars().all()

async def update_user_info(
    db: AsyncSession,
    user_id: int,
    avg_rating: Optional[float] = None,
    genres_preference: Optional[dict] = None,
    tags_preference: Optional[dict] = None,
    svd_vector: Optional[List[float]] = None,
) -> Optional[UserInfoDB]:
    result = await db.execute(select(UserInfoDB).where(UserInfoDB.user_id == user_id))
    db_user_info = result.scalars().first()

    if not db_user_info:
        return None

    if avg_rating is not None:
        db_user_info.avg_rating = avg_rating
    if genres_preference is not None:
        db_user_info.genres_preference = genres_preference
    if tags_preference is not None:
        db_user_info.tags_preference = tags_preference
    if svd_vector is not None:
        db_user_info.svd_vector = svd_vector

    db.add(db_user_info)
    await db.commit()
    await db.refresh(db_user_info)
    return db_user_info