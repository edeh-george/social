from typing import List

from pydantic import BaseModel


class UserPostsIn(BaseModel):
    body: str


class UserPost(UserPostsIn):
    id: int


class CommentIn(BaseModel):
    body: str
    post_id: int


class Comment(CommentIn):
    id: int


class UserPostWithComments(UserPost):
    comments: List[Comment] = []
 