from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#internal:
from .config.main import settings
from .features.user.main import router as user_router
from .features.admin.main import router as admin_router
from .features.common.main import router as common_router
from .features.auth.main import router as auth_router

app = FastAPI()

origins = [settings.CLIENT_PORT]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)
app.include_router(common_router)