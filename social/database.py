import databases
import sqlalchemy
from config import config

metadata = sqlalchemy.MetaData()

post_table = sqlalchemy.Table(
    "posts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
)

user_table = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
)

comment_table = sqlalchemy.Table(
    "comments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("body", sqlalchemy.String),
    sqlalchemy.Column("post_id", sqlalchemy.ForeignKey("posts.id"), nullable=False),
)

engine = sqlalchemy.create_engine(
    config.database_url,
    connect_args={"check_same_thread": False},
)

metadata.create_all(engine)
database = databases.Database(
    config.database_url, force_rollback=config.db_force_rollback
)
