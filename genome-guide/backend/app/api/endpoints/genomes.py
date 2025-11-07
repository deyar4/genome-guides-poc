import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

# Create a directory to store uploaded files
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload/fasta", status_code=201)
async def upload_fasta_file(file: UploadFile = File(...)):
    """
    Accepts a FASTA file upload and saves it to the server.
    """
    if not (file.filename.endswith(".fa") or file.filename.endswith(".fasta")):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .fa or .fasta file.")

    # Sanitize the filename to prevent security issues
    safe_filename = Path(file.filename).name
    destination = UPLOAD_DIR / safe_filename

    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()
    
    return {"filename": safe_filename, "content_type": file.content_type, "path": str(destination)}