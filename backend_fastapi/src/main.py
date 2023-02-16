from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
#internal:
from .config.main import settings

app = FastAPI()

origins = [settings.CLIENT_PORT]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
