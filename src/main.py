from fastapi import FastAPI
from src.config import settings
from src.api.user.router import router as user_router


app = FastAPI()
app.include_router(user_router, prefix="/users", tags=["users"])

print(settings.model_dump())


@app.get("/")
async def root():
    return {"message": "Hello World"}
