from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ADD THIS IMPORT
from .database import engine, init_db
from .models import Base
from .api import genes, genome, variants

# Initialize database
Base.metadata.create_all(bind=engine)
init_db()

app = FastAPI(
    title="Genome Guide API",
    description="Backend for Genome Guide Bioinformatics Platform",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(genes.router, prefix="/genes", tags=["genes"])
app.include_router(genome.router, prefix="/genome", tags=["genome"])
app.include_router(variants.router, prefix="/variants", tags=["variants"])

@app.get("/")
def root():
    return {"message": "Genome Guide API is running"}