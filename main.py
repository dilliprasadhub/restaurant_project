from fastapi import FastAPI

from src.controller.restaurant_controller import router as restaurant_router

app=FastAPI()

app.include_router(restaurant_router)