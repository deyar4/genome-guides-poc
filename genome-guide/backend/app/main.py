from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db.session import engine
from .models import chromosome
from .api.api_v1 import api_router

chromosome.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Genome Guides API",
    description="An API for browsing and searching human genome data.",
    version="0.1.0",
)


# --- CORS MIDDLEWARE ---
# This allows frontend to make requests to your backend.
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -----------------------------------------


@app.get("/")
def read_root():
    return {"message": "Welcome to the Genome Guides API!"}

app.include_router(api_router, prefix="/api/v1")