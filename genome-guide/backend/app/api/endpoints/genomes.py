import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks # Added BackgroundTasks

from ...utils.config_manager import run_snakemake_workflow, read_config # Import Snakemake trigger and config reader

router = APIRouter()

# Create a directory to store uploaded files
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload/fasta", status_code=201)
async def upload_fasta_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    Accepts a FASTA file upload and saves it to the server, then triggers Snakemake workflow.
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
    
    # Get current GTF file path from config
    current_config = read_config()
    current_gtf_path_str = current_config.get("gtf_file")
    current_gtf_path = Path(current_gtf_path_str) if current_gtf_path_str else None

    # Trigger Snakemake workflow in the background
    background_tasks.add_task(run_snakemake_workflow, fasta_file_path=destination, gtf_file_path=current_gtf_path)
    
    return {"filename": safe_filename, "content_type": file.content_type, "path": str(destination), "message": "FASTA file uploaded and Snakemake workflow triggered."}

@router.post("/upload/gtf", status_code=201)
async def upload_gtf_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    Accepts a GTF file upload and saves it to the server, then triggers Snakemake workflow.
    """
    if not (file.filename.endswith(".gtf") or file.filename.endswith(".gff")):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .gtf or .gff file.")

    safe_filename = Path(file.filename).name
    destination = UPLOAD_DIR / safe_filename

    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()
    
    # Get current FASTA file path from config
    current_config = read_config()
    current_fasta_path_str = current_config.get("fasta_file")
    current_fasta_path = Path(current_fasta_path_str) if current_fasta_path_str else None

    # Trigger Snakemake workflow in the background
    background_tasks.add_task(run_snakemake_workflow, fasta_file_path=current_fasta_path, gtf_file_path=destination)
    
    return {"filename": safe_filename, "content_type": file.content_type, "path": str(destination), "message": "GTF file uploaded and Snakemake workflow triggered."}