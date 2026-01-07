import yaml
from pathlib import Path
import logging
import subprocess # Added import
import os # Added import
from typing import Optional # Added import

logger = logging.getLogger(__name__)

CONFIG_PATH = Path(__file__).parent.parent.parent / "config.yaml"
SNAKEFILE_PATH = Path(__file__).parent.parent.parent / "Snakefile" # Added constant
BACKEND_ROOT = Path(__file__).parent.parent.parent # Added constant


def read_config():
    """Reads the Snakemake config.yaml file."""
    if not CONFIG_PATH.exists():
        logger.error(f"Config file not found at {CONFIG_PATH}")
        raise FileNotFoundError(f"Config file not found at {CONFIG_PATH}")
    try:
        with open(CONFIG_PATH, 'r') as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        logger.error(f"Error parsing config.yaml: {e}")
        raise
    except IOError as e:
        logger.error(f"Error reading config.yaml: {e}")
        raise

def update_config(updates: dict):
    """
    Updates specified fields in the config.yaml file.
    
    Args:
        updates (dict): A dictionary of key-value pairs to update in the config.
                        e.g., {"fasta_file": "new_fasta.fa", "gtf_file": "new_gtf.gtf"}
    """
    config = read_config()
    for key, value in updates.items():
        config[key] = value
    
    try:
        with open(CONFIG_PATH, 'w') as f:
            yaml.safe_dump(config, f)
        logger.info(f"Updated config.yaml with: {updates}")
    except IOError as e:
        logger.error(f"Error writing to config.yaml: {e}")
        raise

def run_snakemake_workflow(fasta_file_path: Optional[Path] = None, gtf_file_path: Optional[Path] = None):
    """
    Triggers the Snakemake workflow as a background process.
    Updates config.yaml with provided file paths, or uses existing paths if None.

    Args:
        fasta_file_path (Optional[Path]): The path to the uploaded FASTA file.
        gtf_file_path (Optional[Path]): The path to the uploaded GTF file.
    """
    try:
        current_config = read_config()
        updates = {}

        if fasta_file_path:
            updates["fasta_file"] = str(fasta_file_path)
        else:
            updates["fasta_file"] = current_config.get("fasta_file", "") # Use existing or empty

        if gtf_file_path:
            updates["gtf_file"] = str(gtf_file_path)
        else:
            updates["gtf_file"] = current_config.get("gtf_file", "") # Use existing or empty

        update_config(updates)
        
        command = [
            "snakemake",
            "--snakefile", str(SNAKEFILE_PATH),
            "--configfile", str(CONFIG_PATH),
            "--cores", "1",  # Run with 1 core for simplicity in background task
            "all"  # Target the 'all' rule
        ]
        
        logger.info(f"Triggering Snakemake workflow: {' '.join(command)}")
        
        # Run Snakemake as a detached background process
        process = subprocess.Popen(
            command,
            cwd=BACKEND_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  # Decode stdout/stderr as text
            start_new_session=True # Ensures the child process is detached from the current process group
        )
        
        # Log stdout and stderr asynchronously (or after process finishes)
        # For true background processing without blocking, consider redirecting to files
        # or using a more sophisticated task queue like Celery.
        # For this implementation, we'll log its start and let it run.
        
        logger.info(f"Snakemake workflow triggered with PID: {process.pid}")
        # Optionally, you could store the PID to monitor the process status later
        
    except Exception as e:
        logger.error(f"Failed to trigger Snakemake workflow: {e}", exc_info=True)
        raise