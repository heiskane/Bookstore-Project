from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.api import api_router
from app import models
from app.database import engine

models.Base.metadata.create_all(bind=engine, checkfirst=True)

description = """

Backend API for the Bookstore project

"""

app = FastAPI(description=description)

# https://fastapi.tiangolo.com/tutorial/cors/
# Allowed origins required to allow react to communicate from "diffrent origin"
# Will have to chech if a subdomain is "diffrent origin"
origins = [
    "*",
]

# https://stackoverflow.com/questions/60680870/cors-issues-when-running-a-dockerised-fastapi-application
# for some reason without an endpoint before CORS the cors fails in docker-compose
@app.get("/")
def health_check():
    return {"detail": "I am aliiiiiive"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],  # Allow frontend to get filename
)

app.include_router(api_router)
