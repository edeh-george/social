from typing import List

from pydantic import BaseModel, ConfigDict


class UserPostsIn(BaseModel):
    body: str


class UserPost(UserPostsIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


class CommentIn(BaseModel):
    body: str
    post_id: int


class Comment(CommentIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


class UserPostWithComments(UserPost):
    comments: List[Comment] = []
