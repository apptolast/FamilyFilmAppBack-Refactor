from dotenv import load_dotenv
from fastapi import FastAPI
from config.firebase import initialize_firebase
from router.users import router as users_router
from router.groups import router as groups_router
import os 

load_dotenv()

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

# Init Firebase Admin SDK and get the app
initialize_firebase()


app.include_router(users_router)
app.include_router(groups_router)