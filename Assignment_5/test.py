from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_valid_loan_below_30lac():
    response = client.post("/getLoanDetails", json={"loan_amount": 2000000, "tenure_years": 10})
    assert response.status_code == 200
    data = response.json()
    assert data["total_interest"] > 0
    assert data["total_amount"] > 0

def test_valid_loan_50lac():
    response = client.post("/getLoanDetails", json={"loan_amount": 5000000, "tenure_years": 5})
    assert response.status_code == 200
    data = response.json()
    assert round(data["total_interest"], 2) == round(5000000 * 7.5 * 5 / 100, 2)

def test_invalid_loan_amount():
    response = client.post("/getLoanDetails", json={"loan_amount": 10000000, "tenure_years": 5})
    assert response.status_code == 400
    assert "exceeds supported range" in response.json()["detail"]

def test_negative_tenure():
    response = client.post("/getLoanDetails", json={"loan_amount": 2000000, "tenure_years": -5})
    assert response.status_code == 422  # validation error from Pydantic

def test_pdf_generation():
    response = client.post("/getLoanDetailsPDF", json={"loan_amount": 2000000, "tenure_years": 10})
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
