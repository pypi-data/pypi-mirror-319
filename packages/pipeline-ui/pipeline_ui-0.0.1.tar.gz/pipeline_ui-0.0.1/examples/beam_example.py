import importlib.util
from typing import Any, Dict, Optional
import sys

from beam import Image, function, Output
from fastapi import FastAPI, HTTPException, Request, Response

def load_module_without_server(file_path: str, start_server: bool = True, enable_io_redirect: bool = False):
    from pipeline_ui.modules.pui.pui import PipelineUI
    # Temporarily modify PipelineUI to prevent server start
    original_start = PipelineUI.start
    if not start_server:
        PipelineUI.start = lambda self: None

    if enable_io_redirect:
        PipelineUI.get_io_redirect_state = lambda self: True

    spec = importlib.util.spec_from_file_location("dynamic_module", file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["dynamic_module"] = module
    spec.loader.exec_module(module)

    # Restore original start method
    PipelineUI.start = original_start

    pui_instance = module.pui
    return pui_instance

pui = load_module_without_server("examples/simple.py", start_server=False, enable_io_redirect=False)

@function(
        gpu="T4",
        image=Image().add_python_packages(
            [
                "typer", 
                "requests", 
                "pynput", 
                "watchfiles", 
                "aiohttp", 
                "pillow", 
                "devtools", 
                "toml", 
                "python-dotenv", 
                # the list of dependency that are specific to the workflow
                "torch", 
                "diffusers", 
                "pillow",
                "transformers",
                "accelerate",
            ]
        ),
    )
def run_workflow(workflow_name: str, workflow_inputs: Optional[Dict[str, Any]] = None):
    if workflow_name not in pui.workflows:
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
        last_message = message
        if message.get("func_type") == "workflow" and message.get("status") == "completed":
            break

    return last_message

app = FastAPI()

def create_endpoint(workflow_name: str):
    async def endpoint(request: Request, workflow_inputs: Optional[Dict[str, Any]] = None):
        is_local = request.headers.get("x-run-mode") == "local"
        is_local = True
        if is_local:
            response = run_workflow.local(workflow_name=workflow_name, workflow_inputs=workflow_inputs)
        else:
            response = run_workflow.remote(workflow_name=workflow_name, workflow_inputs=workflow_inputs)
        
        print("response", response)
        func_output = response.get("func_output")
        func_output.show()

        # TODO use temporaly file from beam 
        # TODO load all of this from a database entry and not code

        # add all the return object to the response of the stream
        # {"name":"simple_workflow","status":"completed","func_type":"workflow","duration":"32.47s","artifact_id":"704e07c8-2005-48ce-bbea-cd32b668d1d8","artifact_url":"localhost:8114/api/workflows/artifacts/704e07c8-2005-48ce-bbea-cd32b668d1d8"}
        if "func_output" in response:
            del response["func_output"]
        return response
    return endpoint

# Create endpoints for each workflow
for workflow_name in pui.workflows:
    app.add_api_route(
        f"/api/workflows/{workflow_name.lower()}", 
        create_endpoint(workflow_name),
        methods=["POST"]
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)