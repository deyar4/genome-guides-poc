from fastapi.testclient import TestClient
import pytest

def test_get_gene_correlation_statistic(client: TestClient):
    response = client.get("/api/v1/statistics/gene_density_length_correlation")
    assert response.status_code == 200
    data = response.json()
    assert data["stat_name"] == "gene_density_length_correlation"
    assert isinstance(data["stat_value"], dict)
    assert "correlation_coefficient" in data["stat_value"]
    assert "p_value" in data["stat_value"]
    assert "chromosome_data" in data["stat_value"]
    assert isinstance(data["stat_value"]["chromosome_data"], list)
    
    # Check if chr1 is present in the data
    chr1_data = next((item for item in data["stat_value"]["chromosome_data"] if item["chromosome"] == "chr1"), None)
    assert chr1_data is not None
    assert "density" in chr1_data
    assert "average_gene_length" in chr1_data
    assert chr1_data["gene_count"] >= 1
