#!/bin/bash
set -e

echo "==================================================="
echo "   GENOME GUIDE: FULL PIPELINE BENCHMARK (hg38)"
echo "==================================================="

cd genome-guide/backend

# 1. Clean previous run
echo "[1/3] Cleaning previous database and artifacts..."
snakemake clean --cores 1
rm -f genome_guides.db  # Ensure hard delete for fresh ingestion benchmark
echo "      Clean complete."

# 2. Run Pipeline with Time Measurement
echo "[2/3] Running Full Pipeline (Ingestion + Analysis)..."
echo "      This involves parsing 3GB+ FASTA and full GTF."
echo "      Please wait..."

snakemake --unlock # Ensure no stale locks

start_time=$(date +%s)

# Run snakemake with 1 core to be safe/sequential, or -j for parallel if safe.
# Using -j1 ensures we don't hit SQLite locking issues heavily, though we handle them.
# Using --cores 4 for better performance on parsing/analysis if independent.
# Analysis steps depend on DB, so they might serialize naturally on the DB lock, 
# but parallel execution is better for non-DB CPU work.
# Let's use standard run.
snakemake --cores 4

end_time=$(date +%s)
duration=$((end_time - start_time))

echo "==================================================="
echo "   PIPELINE COMPLETE"
echo "==================================================="
echo "Total Execution Time: $duration seconds"
echo "==================================================="

# 3. Run Granular Analysis Benchmarks
echo "[3/3] Running Granular Analysis Benchmarks (stats)..."
python benchmarks/benchmark_runner.py
