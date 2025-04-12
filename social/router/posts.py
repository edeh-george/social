import logging
from typing import Optional

from database import comment_table, database, post_table
from models.post import Comment, UserPost, UserPostsIn, UserPostWithComments

from fastapi import APIRouter, HTTPException

router = APIRouter()

logger = logging.getLogger(__name__)


async def find_post(post_id: int):
    logger.info(f"Finding post with id {post_id}")
    query = post_table.select().where(post_table.id == post_id)
    logger.debug(query)
    return await database.fetch_one(query)


@router.post("/", response_model=Optional[UserPost], status_code=201)
async def create_post(post: UserPostsIn):
    logger.info("Creating new post")
    data = post.model_dump()
    query = post_table.insert().values(data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@router.get("/post", response_model=list[UserPost])
async def get_all_posts():
    logger.info("Getting all posts")
    query = post_table.select()
    logger.debug(query)
    return await database.fetch_all(query)


@router.post("/", response_model=Comment)
async def create_comment(comment: Comment):
    post = await find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, details="Posts not found")
    data = comment.model_dump()
    query = database.insert().values(data)
    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}


@router.get("/post/{post_id}/comment", response_model=list[Comment])
async def get_comments_on_post(post_id: int):
    logger.info("Getting comments on post")
    query = comment_table.select().where(
        comment_table.post_id == post_id
    )  # in the tutorial the guy did a comment_table.c.post_id. I don't know where he got the 'c' from
    logger.debug(query)
    return await database.fetch_all(query)


@router.get("/post/{post_id}", response_model=UserPostWithComments)
async def get_post_with_comments(post_id: int):
    logger.info("Getting poast and its comments")
    post = await find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {
        "post": post,
        "comments": await get_comments_on_post(post_id),
    }
