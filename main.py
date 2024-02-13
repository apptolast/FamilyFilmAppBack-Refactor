from fastapi import FastAPI
from router import users,group

app = FastAPI()

app.include_router(users.router)
app.include_router(group.router)

