import pytest


@pytest.fixture(scope="function")
def example_workflow_client():
    from typing import Annotated

    import torch
    from diffusers.pipelines.pipeline_utils import DiffusionPipeline
    from diffusers.schedulers.scheduling_dpmsolver_multistep import DPMSolverMultistepScheduler
    from PIL import Image

    from pipeline_ui import (
        ImageInput,
        ImageOutput,
        NodeInput,
        NodeOutput,
        NodePosition,
        PipelineUI,
        TextParameter,
        node,
        workflow,
    )

    pui = PipelineUI()

    @node()
    def load_model(
        model_id = TextParameter(description="The model to load", default="stable-diffusion-v1-5/stable-diffusion-v1-5")
    ) -> Annotated[DiffusionPipeline, NodeOutput(description="The loaded pipeline", name="pipeline")]:
        if torch.backends.mps.is_available():
            device = "mps"
        elif torch.cuda.is_available():
            device = "cuda"
        else:
            device = "cpu"
        pipeline = DiffusionPipeline.from_pretrained(model_id, use_safetensors=True, torch_dtype=torch.float16).to(device)
        pipeline.scheduler = DPMSolverMultistepScheduler.from_config(pipeline.scheduler.config)
        print("hello_1")

        return pipeline

    @node()
    def get_prompt(
        prompt: str = TextParameter(description="The prompt to use for generation", default="A beautiful image")
    ) -> Annotated[str, NodeOutput(description="The prompt to use for generation", name="prompt")]:
        return prompt

    @node()
    def generate_image(
        pipeline: DiffusionPipeline = NodeInput(python_type=DiffusionPipeline, description="The pipeline to use for generation"),
        positive_prompt: str = NodeInput(python_type=str, description="The prompt to use for generation")
    ) -> Annotated[Image.Image, ImageOutput(description="The generated image", name="image")]:
        return pipeline(positive_prompt).images[0]

    @node()
    def save_image(
        image: Image.Image = ImageInput(description="The image to save", render=True)
    ) -> None:
        image.save("image.png")



    @workflow(positions=[
        NodePosition(x=-115, y=-377, node="load_model"),
        NodePosition(x=-110, y=-122, node="get_prompt"), 
        NodePosition(x=197, y=-267, node="generate_image"),
        NodePosition(x=484, y=-250, node="save_image"),
    ])
    def simple_workflow(
        model_id = TextParameter(description="The model to load", default="stable-diffusion-v1-5/stable-diffusion-v1-5"),
        prompt = TextParameter(description="The prompt to use for generation", default="A beautiful image")
    ) -> Annotated[Image.Image, ImageOutput(description="The image to save", name="image", render=True)]:
        """_summary_

        Returns:
            _type_: _description_
        """
        print(f"[DEBUG] load_model func ID in workflow: {id(load_model)} for {load_model.__name__}")
        model = load_model(model_id)
        print("hello_2") # debug print keyerror
        print(f"[DEBUG] get_prompt func ID in workflow: {id(get_prompt)} for {get_prompt.__name__}")

        positive_prompt = get_prompt(prompt)
        # raise
        image = generate_image(model, positive_prompt)
        save_image(image)


        return image


    pui.define_pack(
        name="Simple",
        description="A simple example workflow",
    )

    return pui.start(testing=True)


