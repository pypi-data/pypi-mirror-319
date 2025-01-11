import importlib.util
from typing import Any, Dict, Optional
import sys
from tempfile import NamedTemporaryFile

from beam import Image, function, Output
from fastapi import FastAPI, HTTPException, Request, Response

ENABLE_BEAM = True

def get_workflow_code():
    from examples.simplestr import get_code_string
    # Mock database fetch - in reality this would be a DB query
    return get_code_string()

def load_module_from_string(code_string: str, enable_io_redirect: bool = False):
    """Load a module from a string by writing it to a temporary file first"""
    try:
        # Write the code to a temporary file
        with NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp_file:
            tmp_file.write(code_string)
            tmp_file.flush()
            
            print("Loading module from temporary file:", tmp_file.name)
            
            from pipeline_ui.modules.pui.pui import PipelineUI
            # Temporarily modify PipelineUI to prevent server start
            original_start = PipelineUI.start
            PipelineUI.start = lambda self: None

            if enable_io_redirect:
                PipelineUI.get_io_redirect_state = lambda self: True

            # Load module from the temporary file
            spec = importlib.util.spec_from_file_location("dynamic_module", tmp_file.name)
            if spec is None or spec.loader is None:
                raise ImportError("Failed to create module specification")
                
            module = importlib.util.module_from_spec(spec)
            sys.modules["dynamic_module"] = module
            spec.loader.exec_module(module)

            # Restore original start method
            PipelineUI.start = original_start

            if not hasattr(module, 'pui'):
                raise AttributeError("Module does not contain 'pui' instance")
                
            print("Successfully loaded module")
            return module.pui
            
    except Exception as e:
        print("Error loading module:", str(e))
        raise RuntimeError(f"Failed to load module: {str(e)}")

# Initialize PUI from code string

@function(
    gpu="T4",
    image=Image().add_python_packages([
        "typer", "requests", "pynput", "watchfiles", "aiohttp", 
        "pillow", "devtools", "toml", "python-dotenv",
        "torch", "diffusers", "pillow", "transformers", "accelerate",
        "safetensors",
    ]),
)
def run_workflow(workflow_name: str, workflow_inputs: Optional[Dict[str, Any]] = None):
    print(f"Running workflow: {workflow_name}")
    if workflow_inputs:
        print("With inputs:", workflow_inputs)
    
    pui = load_module_from_string(get_workflow_code(), enable_io_redirect=False)
    if workflow_name not in pui.workflows:
        print(f"Workflow '{workflow_name}' not found in available workflows:", list(pui.workflows.keys()))
        raise HTTPException(status_code=404, detail=f"Workflow '{workflow_name}' not found")

    workflow = pui.workflows[workflow_name]
    func = workflow.func

    # Execute workflow to generate stream
    if workflow_inputs:
        func(**workflow_inputs)
    else:
        func()

    # Get messages from queue until workflow completion
    last_message = None
    while True:
        message = pui.stream_state_manager.output_queue.get()
        print("Received message:", message)
        last_message = message
        if message.get("func_type") == "workflow" and message.get("status") == "completed":
            break

    return last_message

app = FastAPI()

def create_endpoint(workflow_name: str):
    async def endpoint(request: Request, workflow_inputs: Optional[Dict[str, Any]] = None):
        print(f"Received request for workflow: {workflow_name}")
        print("Request headers:", request.headers)
        print("Workflow inputs:", workflow_inputs)

        if ENABLE_BEAM:
            print("Running workflow remotely with Beam")
            response = run_workflow.remote(workflow_name=workflow_name, workflow_inputs=workflow_inputs)
        else:
            print("Running workflow locally")
            response = run_workflow.local(workflow_name=workflow_name, workflow_inputs=workflow_inputs)
        
        print("Response:", response)
        func_output = response.get("func_output")
        func_output.show()

        if "func_output" in response:
            del response["func_output"]
        return response
    return endpoint

# Create endpoints for each workflow
workflows_names = ["simple_workflow"]
print("Creating endpoints for workflows:", workflows_names)
for workflow_name in workflows_names:
    app.add_api_route(
        f"/api/workflows/{workflow_name.lower()}", 
        create_endpoint(workflow_name),
        methods=["POST"]
    )

if __name__ == "__main__":
    print("Starting server on http://0.0.0.0:8000")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)