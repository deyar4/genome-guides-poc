from fastapi.testclient import TestClient
import pytest

def test_get_cpg_association_statistic(client: TestClient):
    response = client.get("/api/v1/statistics/cpg_island_gene_association")
    assert response.status_code == 200
    data = response.json()
    assert data["stat_name"] == "cpg_island_gene_association"
    assert isinstance(data["stat_value"], dict)
    
    # In conftest.py:
    # Gene is at 11869-14409
    # CpG Island is at 11000-12000
    # Overlap: 11869 <= 12000 and 14409 >= 11000. Yes, they overlap (11869-12000).
    
    assert data["stat_value"]["total_islands"] == 1
    assert data["stat_value"]["associated_with_genes"] == 1
    assert data["stat_value"]["non_associated"] == 0
    assert data["stat_value"]["percentage_associated"] == 100.0
