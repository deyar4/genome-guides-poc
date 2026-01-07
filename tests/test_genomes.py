from fastapi.testclient import TestClient
from pathlib import Path
from io import BytesIO
import pytest

# Assuming UPLOAD_DIR is configured in your main app to be relative to the project root
# For testing, we might want to ensure a clean upload directory or mock the upload process
# For simplicity, we'll let the app manage its own UPLOAD_DIR which should be cleaned by
# the overall test environment teardown if it creates files in a test-specific location.

def test_upload_fasta_success(client: TestClient):
    fasta_content = b">seq1\nAGCT\n>seq2\nTCGA\n"
    # TestClient expects files in the format ('name', ('filename', content, 'content_type'))
    files = {'file': ('test_upload.fasta', BytesIO(fasta_content), 'application/octet-stream')}
    
    response = client.post("/api/v1/genomes/upload/fasta", files=files)
    
    assert response.status_code == 201
    json_response = response.json()
    assert json_response["filename"] == "test_upload.fasta"
    assert "path" in json_response
    assert Path(json_response["path"]).exists() # Verify file creation

    # Clean up the uploaded file to prevent test pollution
    Path(json_response["path"]).unlink()


def test_upload_fasta_invalid_type(client: TestClient):
    invalid_content = b"This is not a fasta file."
    files = {'file': ('test_upload.txt', BytesIO(invalid_content), 'text/plain')}
    
    response = client.post("/api/v1/genomes/upload/fasta", files=files)
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid file type. Please upload a .fa or .fasta file."}


def test_upload_fasta_empty_file(client: TestClient):
    empty_content = b""
    files = {'file': ('empty.fasta', BytesIO(empty_content), 'application/octet-stream')}
    
    response = client.post("/api/v1/genomes/upload/fasta", files=files)
    
    # FastAPI's UploadFile will still create an empty file if the upload is valid
    # but the content is empty. The endpoint logic doesn't explicitly check for
    # empty content. It validates the file extension.
    # So, we expect a 201, and then verify the file is indeed empty.
    assert response.status_code == 201
    json_response = response.json()
    assert json_response["filename"] == "empty.fasta"
    uploaded_path = Path(json_response["path"])
    assert uploaded_path.exists()
    assert uploaded_path.stat().st_size == 0 # Check if the file is empty

    # Clean up the uploaded file
    uploaded_path.unlink()

def test_upload_fasta_no_file_provided(client: TestClient):
    # This scenario tests FastAPI's validation when 'File(...)' is expected but not provided
    response = client.post("/api/v1/genomes/upload/fasta")
    
    # FastAPI should return a 422 Unprocessable Entity for a missing required field
    assert response.status_code == 422
    json_response = response.json()
    assert "detail" in json_response
    assert any("Field required" in error["msg"] for error in json_response["detail"])
