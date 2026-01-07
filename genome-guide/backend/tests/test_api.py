from fastapi.testclient import TestClient
import pytest # Import pytest for potential future use or clarity

def test_read_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Genome Guides API!"}

def test_read_chromosomes(client: TestClient):
    response = client.get("/api/v1/chromosomes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Assuming the dummy data has at least one chromosome
    assert len(data) > 0
    assert data[0]["name"] == "chr1"

def test_search_genes(client: TestClient):
    response = client.get("/api/v1/genes/search/DDX11L1")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["gene_name"] == "DDX11L1"

def test_search_genes_not_found(client: TestClient):
    response = client.get("/api/v1/genes/search/NONEXISTENT")
    assert response.status_code == 404
    assert response.json() == {"detail": "No genes found matching the query"} # Assert JSON structure

def test_read_gene_by_name(client: TestClient):
    response = client.get("/api/v1/genes/DDX11L1")
    assert response.status_code == 200
    data = response.json()
    assert data["gene_name"] == "DDX11L1"

def test_read_gene_by_name_not_found(client: TestClient):
    response = client.get("/api/v1/genes/NONEXISTENT")
    assert response.status_code == 404
    assert response.json() == {"detail": "Gene not found"} # Assert JSON structure

def test_get_statistic(client: TestClient):
    response = client.get("/api/v1/statistics/gc_content_per_chromosome")
    assert response.status_code == 200
    data = response.json()
    assert data["stat_name"] == "gc_content_per_chromosome"
    assert "chr1" in data["stat_value"]
    assert data["stat_value"]["chr1"] == 50.00 # Updated for dummy FASTA

def test_get_statistic_not_found(client: TestClient):
    response = client.get("/api/v1/statistics/NONEXISTENT")
    assert response.status_code == 404
    assert response.json() == {"detail": "Statistic not found"} # Assert JSON structure

def test_get_simple_sequence_repeats(client: TestClient):
    response = client.get("/api/v1/statistics/simple_sequence_repeats")
    assert response.status_code == 200
    data = response.json()
    assert data["stat_name"] == "simple_sequence_repeats"
    assert isinstance(data["stat_value"], dict) # stat_value is now a dict
    assert "ssrs" in data["stat_value"] # Check for the 'ssrs' key
    assert isinstance(data["stat_value"]["ssrs"], list) # The actual list of SSRs
    # The minimal data contains one SSR, so check for len > 0
    assert len(data["stat_value"]["ssrs"]) > 0 
    # Validate the structure of an SSR entry
    ssr_entry = data["stat_value"]["ssrs"][0]
    assert "chromosome_name" in ssr_entry
    assert "motif" in ssr_entry
    assert "count" in ssr_entry
    assert "length" in ssr_entry
    assert "start_position" in ssr_entry
    assert "end_position" in ssr_entry

def test_read_chromosome_lengths(client: TestClient):
    response = client.get("/api/v1/chromosomes/lengths")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "name" in data[0]
    assert isinstance(data[0]["name"], str)
    assert "length" in data[0]
    assert isinstance(data[0]["length"], int)

# --- New tests for global exception handlers ---

def test_http_exception_custom(client: TestClient):
    """
    Tests the custom HTTPException handler using a deliberately crafted endpoint.
    """
    response = client.get("/test-exceptions/raise-http-exception")
    assert response.status_code == 418
    assert response.json() == {"detail": "I'm a teapot exception!"}

def test_generic_exception_handling(client: TestClient):
    """
    Tests the generic Exception handler for unhandled exceptions.
    """
    response = client.get("/test-exceptions/raise-generic-exception")
    assert response.status_code == 500
    assert response.json() == {"detail": "An unexpected error occurred."}

def test_get_centromere_sequence(client: TestClient):
    response = client.get("/api/v1/centromeres/chr1/sequence")
    assert response.status_code == 200
    data = response.json()
    assert data["chromosome_name"] == "chr1"
    assert data["start_position"] == 5
    assert data["end_position"] == 8
    assert data["length"] == 4
    assert data["sequence"] == "ATGC" # Sequence from test_hg38.fa is ATGCATGCATGC, so 5-8 is ATGC

def test_get_telomere_sequences(client: TestClient):
    response = client.get("/api/v1/telomeres/chr1/sequence")
    assert response.status_code == 200
    data = response.json()
    assert "telomeres" in data
    assert isinstance(data["telomeres"], list)
    assert len(data["telomeres"]) == 2 # Expect two telomeres for chr1

    # Validate first telomere
    telomere1 = data["telomeres"][0]
    assert telomere1["chromosome_name"] == "chr1"
    assert telomere1["start_position"] == 1
    assert telomere1["end_position"] == 4
    assert telomere1["length"] == 4
    assert telomere1["sequence"] == "ATGC"

    # Validate second telomere
    telomere2 = data["telomeres"][1]
    assert telomere2["chromosome_name"] == "chr1"
    assert telomere2["start_position"] == 9
    assert telomere2["end_position"] == 12
    assert telomere2["length"] == 4
    assert telomere2["sequence"] == "ATGC"

def test_get_nuclear_base_composition(client: TestClient):
    response = client.get("/api/v1/statistics/nuclear_base_composition")
    assert response.status_code == 200
    data = response.json()
    assert data["stat_name"] == "nuclear_base_composition"
    assert isinstance(data["stat_value"], dict)
    assert "A" in data["stat_value"]
    assert "T" in data["stat_value"]
    assert "C" in data["stat_value"]
    assert "G" in data["stat_value"]
    # Based on dummy fasta ">chr1\nATGCATGCATGC" (length 12)
    assert data["stat_value"]["A"] == 3
    assert data["stat_value"]["T"] == 3
    assert data["stat_value"]["C"] == 3
    assert data["stat_value"]["G"] == 3

def test_get_mitochondrial_base_composition(client: TestClient):
    response = client.get("/api/v1/statistics/mitochondrial_base_composition")
    assert response.status_code == 200
    data = response.json()
    assert data["stat_name"] == "mitochondrial_base_composition"
    assert isinstance(data["stat_value"], dict)
    # Our dummy data doesn't have mitochondrial chromosomes, so it should be empty
    assert len(data["stat_value"]) == 0

def test_get_dinucleotide_frequency(client: TestClient):
    response = client.get("/api/v1/statistics/dinucleotide_frequency")
    assert response.status_code == 200
    data = response.json()
    assert data["stat_name"] == "dinucleotide_frequency"
    assert isinstance(data["stat_value"], dict)
    # Based on dummy fasta ">chr1\nATGCATGCATGC"
    # Dinucleotides: AT, TG, GC, CA, AT, TG, GC, CA, AT, TG, GC
    expected_dinucleotides = {
        "AT": 3,
        "TG": 3,
        "GC": 3,
        "CA": 2
    }
    assert data["stat_value"] == expected_dinucleotides

def test_get_cpg_frequency_per_chromosome(client: TestClient):
    response = client.get("/api/v1/statistics/cpg_frequency_per_chromosome")
    assert response.status_code == 200
    data = response.json()
    assert data["stat_name"] == "cpg_frequency_per_chromosome"
    assert isinstance(data["stat_value"], dict)
    # Based on dummy fasta ">chr1\nATGCATGCATGC" (total dinucleotides: 11, CG count: 0)
    assert data["stat_value"]["chr1"] == 0.00

def test_get_per_chromosome_composition(client: TestClient):
    response = client.get("/api/v1/statistics/per_chromosome_composition")
    assert response.status_code == 200
    data = response.json()
    assert data["stat_name"] == "per_chromosome_composition"
    assert isinstance(data["stat_value"], dict)
    assert "chr1" in data["stat_value"]
    # Based on dummy fasta ">chr1\nATGCATGCATGC"
    expected_composition = {"A": 3, "T": 3, "C": 3, "G": 3}
    assert data["stat_value"]["chr1"] == expected_composition
