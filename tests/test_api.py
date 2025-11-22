
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Scheduling Simulator API. Visit /docs for documentation."}

def test_get_algorithms():
    response = client.get("/api/algorithms")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    
    # Check for new algorithms
    algo_ids = [a['id'] for a in data]
    assert 'FCFS' in algo_ids
    assert 'HRRN' in algo_ids
    assert 'MLF' in algo_ids

def test_run_simulation_fcfs():
    payload = {
        "algorithm": "FCFS",
        "num_machines": 2,
        "tasks": [
            {
                "id": 1,
                "arrival_time": 0,
                "processing_time": 10,
                "priority": "HIGH",
                "deadline": 20,
                "cpu_required": 1,
                "ram_required": 1
            }
        ],
        "alpha": 0.7
    }
    response = client.post("/api/simulate", json=payload)
    assert response.status_code == 200
    result = response.json()
    assert result['total_tasks'] == 1
    assert result['tasks'][0]['id'] == 1
