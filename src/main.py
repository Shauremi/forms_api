from fastapi import FastAPI
from functools import cache
import uvicorn

from src.forms import router as router_forms
from src.users import router as router_users
from src.database import Base, sync_engine


app =  FastAPI(title="Forms API", description="---")
app.include_router(router_forms)
app.include_router(router_users)

Base.metadata.create_all(bind=sync_engine)

if __name__ == '__main__':
    uvicorn.run(
        'src.main',
        host="127.0.0.1",
        port=5000,
        reload=True
    )