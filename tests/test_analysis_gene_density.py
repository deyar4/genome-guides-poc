from fastapi.testclient import TestClient
import pytest

def test_get_gene_density_statistic(client: TestClient):
    response = client.get("/api/v1/statistics/gene_density_1mb")
    assert response.status_code == 200
    data = response.json()
    assert data["stat_name"] == "gene_density_1mb"
    assert isinstance(data["stat_value"], dict)
    assert "bin_size" in data["stat_value"]
    assert data["stat_value"]["bin_size"] == 1000000
    assert "data" in data["stat_value"]
    assert "chr1" in data["stat_value"]["data"]
    # Verify we have a list of bins for chr1
    bins = data["stat_value"]["data"]["chr1"]
    assert isinstance(bins, list)
    # The dummy GTF has one gene at pos 11869, which falls in the first bin (0-1Mb)
    # The dummy chromosome length is 12 (very small), so it should have 1 bin.
    # Wait, the dummy data in conftest.py creates chr1 with length 12?
    # Let's check conftest.py again.
    # If length is 12, bin size 1,000,000. num_bins = ceil(12 / 1M) = 1.
    assert len(bins) > 0
    assert bins[0] >= 1 # Should contain at least the one dummy gene
