code_string = '''import torch
from diffusers.pipelines.pipeline_utils import DiffusionPipeline
from diffusers.schedulers.scheduling_dpmsolver_multistep import DPMSolverMultistepScheduler
from PIL import Image
from typing import Annotated

from pipeline_ui import PipelineUI
from pipeline_ui.modules.node.schema.client.schema import ImageInput, ImageOutput, NodeInput, NodeOutput, TextParameter
from pipeline_ui.modules.workflow.schema.client.schema import NodePosition

model_id = "stable-diffusion-v1-5/stable-diffusion-v1-5"
pipeline = DiffusionPipeline.from_pretrained(model_id, use_safetensors=True)

pui = PipelineUI()

pui.define_pack(
    name="Simple",
    description="A simple example workflow",
)

def get_device():
    if torch.backends.mps.is_available():
        return "mps"
    elif torch.cuda.is_available():
        return "cuda"
    else:
        return "cpu"

@pui.node()
def load_model(
    model_id = TextParameter(description="The model to load", default="stable-diffusion-v1-5/stable-diffusion-v1-5")
) -> Annotated[DiffusionPipeline, NodeOutput(description="The loaded pipeline", name="pipeline")]:
    device = get_device()
    pipeline = DiffusionPipeline.from_pretrained(model_id, use_safetensors=True, torch_dtype=torch.float16).to(device)
    pipeline.scheduler = DPMSolverMultistepScheduler.from_config(pipeline.scheduler.config)

    return pipeline

@pui.node()
def get_prompt(
    prompt: str = TextParameter(description="The prompt to use for generation", default="A beautiful image")
) -> Annotated[str, NodeOutput(description="The prompt to use for generation", name="prompt")]:
    return prompt

@pui.node()
def generate_image(
    pipeline: DiffusionPipeline = NodeInput(python_type=DiffusionPipeline, description="The pipeline to use for generation"),
    positive_prompt: str = NodeInput(python_type=str, description="The prompt to use for generation")
) -> Annotated[Image.Image, ImageOutput(description="The generated image", name="image")]:
    return pipeline(positive_prompt).images[0]

@pui.node()
def save_image(
    image: Image.Image = ImageInput(description="The image to save", render=True)
) -> None:
    image.save("image.png")

positions = [
    NodePosition(x=-115, y=-377, node="load_model"),
    NodePosition(x=-110, y=-122, node="get_prompt"), 
    NodePosition(x=197, y=-267, node="generate_image"),
    NodePosition(x=484, y=-250, node="save_image"),
]

@pui.workflow(positions=positions)
def simple_workflow(
    model_id = TextParameter(description="The model to load", default="stable-diffusion-v1-5/stable-diffusion-v1-5"),
    prompt = TextParameter(description="The prompt to use for generation", default="A beautiful image")
) -> Annotated[Image.Image, ImageOutput(description="The image to save", name="image", render=True)]:
    model = load_model(model_id)
    positive_prompt = get_prompt(prompt)
    image = generate_image(model, positive_prompt)
    save_image(image)

    return image

pui.start()
'''

def get_code_string():
    return code_string
