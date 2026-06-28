from app.db.base import Base
from app.db.session import engine

# import all models so SQLAlchemy knows them
from app.models.user import User  # IMPORTANT

def init_db():
    Base.metadata.create_all(bind=engine)