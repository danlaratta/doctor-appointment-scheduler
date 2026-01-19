from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.settings import settings


# establish asynchronous connection to a database (connects session to database)
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
)

# Creates a factory for generating new asynchronous database sessions (session = the actual communitcation to DB like querying and committing)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

# Dependency to get the DB sessions
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def close_engine():
    await engine.dispose()


