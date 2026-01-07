from fastapi.testclient import TestClient
import pytest

def test_get_utr_correlation_statistic(client: TestClient):
    response = client.get("/api/v1/statistics/utr_transcript_correlation")
    assert response.status_code == 200
    data = response.json()
    assert data["stat_name"] == "utr_transcript_correlation"
    assert isinstance(data["stat_value"], dict)
    
    # Based on conftest.py:
    # Gene DDX11L1 has 2 exons: 10000-12000 (2001) and 15000-17000 (2001). Total = 4002.
    # It has 1 UTR: 10000-10500 (501).
    
    assert data["stat_value"]["total_genes_analyzed"] >= 1
    assert data["stat_value"]["average_transcript_length"] > 0
    assert data["stat_value"]["average_utr_length"] > 0

def test_get_nested_genes_statistic(client: TestClient):
    response = client.get("/api/v1/statistics/nested_genes_statistics")
    assert response.status_code == 200
    data = response.json()
    assert data["stat_name"] == "nested_genes_statistics"
    assert isinstance(data["stat_value"], dict)
    
    # Based on conftest.py:
    # DDX11L1: 10000-20000
    # NESTED1: 13000-14000 (Inside)
    
    assert data["stat_value"]["total_nested_pairs"] >= 1
    found_nested = any(p["inner_gene"] == "NESTED1" and p["outer_gene"] == "DDX11L1" 
                       for p in data["stat_value"]["nested_pairs"])
    assert found_nested
