import pytest
from fastapi.testclient import TestClient
import os
import subprocess
import sys
from fastapi import APIRouter, HTTPException

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Test Exception Router ---
exception_test_router = APIRouter()

@exception_test_router.get("/raise-generic-exception")
async def raise_generic_exception_endpoint():
    """Endpoint that raises a generic exception for testing purposes."""
    raise ValueError("This is a simulated generic exception!")

@exception_test_router.get("/raise-http-exception")
async def raise_http_exception_endpoint():
    """Endpoint that raises an HTTPException for testing purposes."""
    raise HTTPException(status_code=418, detail="I'm a teapot exception!")
# -----------------------------


@pytest.fixture(scope="function") # Changed to function scope
def setup_test_environment():
    """
    Set up the test environment before any tests run.
    """
    backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    env_file = os.path.join(backend_root, "testing.env")
    db_file = os.path.join(backend_root, "test_genome_guides.db")
    # Ensure a clean slate for the test database at the very beginning of the fixture
    if os.path.exists(db_file):
        os.remove(db_file)
    fasta_file = os.path.join(backend_root, "test_hg38.fa")
    gtf_file = os.path.join(backend_root, "test_Homo_sapiens.GRCh38.115.chr.gtf")
    # Create dummy files for testing if they don't exist
    # In a real scenario, you might want to use small fixtures
    backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cpg_file = os.path.join(backend_root, "tests/data/test_cpgIslandExt.txt")
    if not os.path.exists(cpg_file):
        with open(cpg_file, "w") as f:
            f.write("chr1\t100\t200\tCpG: 10\n")
    config_file = os.path.join(backend_root, "test_config.yaml")
    # Create a test-specific alembic.ini
    alembic_ini_file = os.path.join(backend_root, "test_alembic.ini")

    with open(env_file, "w") as f:
        f.write(f"SQLALCHEMY_DATABASE_URL=sqlite:///{db_file}\n") # Use db_file directly
        f.write('CORS_ORIGINS=["http://localhost:3000"]\n')
        
    with open(fasta_file, "w") as f:
        f.write(">chr1\nATGCATGCATGC\n") # Changed to include an SSR

    with open(gtf_file, "w") as f:
        # Parent Gene
        f.write('1\tensembl_havana\tgene\t10000\t20000\t.\t+\t.\tgene_id "ENSG00000223972"; gene_version "5"; gene_name "DDX11L1"; gene_source "ensembl_havana"; gene_biotype "transcribed_unprocessed_pseudogene";\n')
        # Exon for parent
        f.write('1\tensembl_havana\texon\t10000\t12000\t.\t+\t.\tgene_id "ENSG00000223972"; exon_number "1";\n')
        f.write('1\tensembl_havana\texon\t15000\t17000\t.\t+\t.\tgene_id "ENSG00000223972"; exon_number "2";\n')
        # UTR for parent
        f.write('1\tensembl_havana\tUTR\t10000\t10500\t.\t+\t.\tgene_id "ENSG00000223972";\n')
        
        # Nested Gene (entirely inside 10000-20000)
        f.write('1\tensembl_havana\tgene\t13000\t14000\t.\t+\t.\tgene_id "ENSG_NESTED_1"; gene_name "NESTED1";\n')


    with open(cpg_file, "w") as f:
        # UCSC format: bin chrom chromStart chromEnd name length cpgNum gcNum perGc perCpg
        # Note: '1' for chrom will be mapped to 'chr1' by parser
        f.write('585\t1\t11000\t12000\tCpG: 100\t1000\t50\t600\t60\t10\n')

    with open(config_file, "w") as f:
        f.write('genome: hg38\n')
        f.write(f'fasta_file: "{os.path.basename(fasta_file)}"\n') # Use basename for config
        f.write(f'gtf_file: "{os.path.basename(gtf_file)}"\n')
        f.write(f'cpg_island_file: "{os.path.basename(cpg_file)}"\n')

    # Set environment variables for subprocesses and application settings
    os.environ["ENV_FILE"] = env_file
    os.environ["PYTEST_RUNNING"] = "true"
    os.environ["SQLALCHEMY_DATABASE_URL"] = f"sqlite:///{db_file}" # Use absolute path for consistency

    # Create a copy of the current environment and add the backend_root to PYTHONPATH
    updated_env = os.environ.copy()
    current_python_path = updated_env.get("PYTHONPATH", "")
    if backend_root not in current_python_path:
        updated_python_path = f"{backend_root}:{current_python_path}" if current_python_path else backend_root
        updated_env["PYTHONPATH"] = updated_python_path
    
    try: # This try block starts here, encompassing all setup
        # Unlock snakemake directory in case of previous failed runs
        subprocess.run(["snakemake", "--unlock"], cwd=backend_root, check=True, env=updated_env) # Pass the updated environment
        # Run the snakemake pipeline to create and populate the test database
        subprocess.run(
            ["snakemake", "--cores", "1", "all", "--forceall", "--configfile", config_file],
            cwd=backend_root,
            check=True,
            env=updated_env # Pass the updated environment
        )

        yield # Yield control to the client fixture

    finally:
        # Teardown: clean up the test database and files
        subprocess.run(["snakemake", "--cores", "1", "clean", "--configfile", config_file], cwd=backend_root, check=True, env=updated_env) # Pass the updated environment
        if os.path.exists(env_file):
            os.remove(env_file)
        if os.path.exists(db_file):
            os.remove(db_file)
        if os.path.exists(fasta_file):
            os.remove(fasta_file)
        if os.path.exists(gtf_file):
            os.remove(gtf_file)
        if os.path.exists(config_file):
            os.remove(config_file)

@pytest.fixture
def client(setup_test_environment):
    """
    Get a TestClient instance that reads from the test .env file.
    This fixture depends on setup_test_environment to ensure the database is ready.
    """
    # Dynamically import necessary modules here to ensure sys.path is correctly set
    from app.config import reload_settings
    from app.db.session import reset_db_connection
    from app.main import create_app
    # Reload app settings to pick up the test environment variables
    reload_settings() # Call after env vars set
    reset_db_connection() # Force re-creation of the engine

    app = create_app()
    # Include the test exception router
    app.include_router(exception_test_router, prefix="/test-exceptions")
    with TestClient(app, raise_server_exceptions=False) as client: # Added raise_server_exceptions=False
        yield client


