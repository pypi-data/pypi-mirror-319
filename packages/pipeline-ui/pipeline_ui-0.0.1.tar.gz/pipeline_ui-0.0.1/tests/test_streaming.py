import pytest


@pytest.mark.timeout(45)
def test_workflow_streaming(example_workflow_client):
    client = example_workflow_client
    response = client.post("/api/workflows/stream/simple_workflow", json=[])
    assert response.status_code == 200
    
    events = response.json()
    assert len(events) == 10
    
    # Check workflow start
    assert events[0] == {
        "name": "simple_workflow",
        "status": "started",
        "func_type": "workflow"
    }
    
    # Check load_model node
    assert events[1] == {
        "name": "load_model",
        "status": "started", 
        "func_type": "node"
    }
    assert events[2]["name"] == "load_model"
    assert events[2]["status"] == "completed"
    assert events[2]["func_type"] == "node"
    assert "duration" in events[2]
    
    # Check get_prompt node
    assert events[3] == {
        "name": "get_prompt",
        "status": "started",
        "func_type": "node"
    }
    assert events[4]["name"] == "get_prompt" 
    assert events[4]["status"] == "completed"
    assert events[4]["func_type"] == "node"
    assert "duration" in events[4]
    
    # Check generate_image node
    assert events[5] == {
        "name": "generate_image",
        "status": "started",
        "func_type": "node"
    }
    assert events[6]["name"] == "generate_image"
    assert events[6]["status"] == "completed"
    assert events[6]["func_type"] == "node"
    assert "duration" in events[6]
    
    # Check save_image node
    assert events[7]["name"] == "save_image"
    assert events[7]["status"] == "started"
    assert events[7]["func_type"] == "node"
    assert "artifact_id" in events[7]
    assert "artifact_url" in events[7]
    
    assert events[8]["name"] == "save_image"
    assert events[8]["status"] == "completed"
    assert events[8]["func_type"] == "node"
    assert "duration" in events[8]
    
    # Check workflow completion
    assert events[9]["name"] == "simple_workflow"
    assert events[9]["status"] == "completed"
    assert events[9]["func_type"] == "workflow"
    assert "duration" in events[9]
    assert "artifact_id" in events[9]
    assert "artifact_url" in events[9]
