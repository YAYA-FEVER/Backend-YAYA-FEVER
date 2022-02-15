from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import admin, customer, hardware, user

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router)
app.include_router(customer.router)
app.include_router(hardware.router)
app.include_router(user.router)



                