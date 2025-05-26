from fastapi import FastAPI
from routes.routes import router

app = FastAPI()
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Api de productos"}