# Genome Guides - Backend

This is the backend for the Genome Guides project, a bioinformatics engine designed to answer genomic questions programmatically. It utilizes FastAPI for the API layer, SQLite (development) for storage, and Snakemake for orchestrating genomic data analysis pipelines.

## Project Structure

- **app/**: The FastAPI application (models, schemas, API endpoints).
- **analysis/**: Python scripts for genomic statistical analysis.
- **scripts/**: Data parsers and utility scripts.
- **uploads/**: Storage for raw genomic data files (FASTA, GTF, BED).
- **Snakefile**: The pipeline definition for ETL and analysis tasks.
- **config.yaml**: Configuration for the Snakemake pipeline.

## Prerequisites

- Python 3.10+
- `pip` or `uv` (for package management)

## Setup

1.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Download Data:**
    Ensure you have the necessary genomic data files in the `uploads/` directory as specified in `config.yaml`:
    - `hg38.fa` (Genome Sequence)
    - `Homo_sapiens.GRCh38.115.chr.gtf` (Gene Annotations)
    - `cpgIslandExt.txt` (CpG Islands)
    - `rmsk.txt` (RepeatMasker)

## Usage

### Running the Analysis Pipeline
To ingest data and calculate genomic statistics, run the Snakemake workflow:

```bash
snakemake --cores 1
```
*Note: Use `--cores N` to run N jobs in parallel.*

### Running the API Server
To start the FastAPI development server:

```bash
./run_dev.sh
```
Or manually:
```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.
API Documentation (Swagger UI): `http://localhost:8000/docs`.

## Testing

Run the test suite using `pytest`:

```bash
pytest tests
```

## Architecture

1.  **ETL**: Raw files -> Parsers (`scripts/`) -> SQLite Database.
2.  **Analysis**: Scripts (`analysis/`) query the DB -> Compute Stats -> Update `genome_stats` table.
3.  **Serving**: FastAPI endpoints (`app/api/`) query the `genome_stats` table -> JSON response.