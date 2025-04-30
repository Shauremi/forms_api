from fastapi import FastAPI
import uvicorn

from src.users import router as router_users
from src.database import Base, engine

app = FastAPI(title="Users API", description="---")
app.include_router(router_users)

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("src.main", host="127.0.0.1", port=5000, reload=True)
