from db_setup import engine, Base
from models import users, posts, groups, comments, base

Base.metadata.create_all(bind=engine)