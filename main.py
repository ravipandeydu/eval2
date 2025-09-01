from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
from db.database import init_db
from routes.user_route import user_router
from routes.wallet_route import wallet_router
from routes.transfer_route import transfer_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(user_router)
app.include_router(wallet_router)
app.include_router(transfer_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
