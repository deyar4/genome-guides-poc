#!/usr/bin/env bash
set -euo pipefail

# If you use fish, run: `bash run_dev.sh`

python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

export PYTHONPATH=$(pwd)
uvicorn app.main:app --reload --port 8000