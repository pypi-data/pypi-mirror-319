from enum import Enum
from typing import Annotated

from pipeline_ui import PipelineUI
from pipeline_ui.modules.node.schema.client.schema import (
    NodeInput,
    NodeOutput,
    NumberParameter,
    RadioParameter,
    TextParameter,
)
from pipeline_ui.modules.workflow.schema.client.schema import NodePosition

pui = PipelineUI()

@pui.node(name="KSampler")
def k_sampler(
    model: str = NodeInput(python_type=str, description="The model to use for sampling"),
    positive = NodeInput(python_type=str, description="Positive prompt for guidance"),
    negative = NodeInput(python_type=str, description="Negative prompt for guidance"),
    latent_image = NodeInput(python_type=str, description="The latent image to denoise"),
    seed = NumberParameter(default=5, description="Random seed for generation", min=0, max=9),
    control_after_generate = RadioParameter(
        default="randomize",
        description="Action to take with the seed after generation",
        options=["randomize", "keep"],
    ),
    steps = NumberParameter(default=20, description="Number of denoising steps", min=1, max=100),
    cfg = NumberParameter(default=8, description="Classifier Free Guidance scale", min=1, max=30),
    sampler_name = RadioParameter(
        default="euler",
        description="Name of the sampler to use",
        options=[
            "euler",
            "euler_ancestral", 
            "euler_cfg_pp",
            "heun",
            "heunpp2",
            "dpm_2",
            "dpm_2_ancestral",
        ],
    ),
    scheduler = RadioParameter(
        default="normal",
        description="Type of scheduler to use",
        options=["normal", "advanced"],
    ),
    denoise = NumberParameter(description="Strength of denoising", min=0.0, max=1.0, default=1.0),
) -> Annotated[str, NodeOutput(description="The denoised image", name="LATENT")]:
    """_summary_

    Returns:
        _type_: _description_
    """
    # Perform sampling logic and return the result
    return f"Generated with {model}"

@pui.node(name="Load Checkpoint")
def load_checkpoint(
    ckpt_name = TextParameter(default="", description="Checkpoint file to load"),
) -> tuple[
    Annotated[str, NodeOutput(description="The loaded model", name="MODEL")],
    Annotated[str, NodeOutput(description="The loaded CLIP model", name="CLIP")],
    Annotated[str, NodeOutput(description="The loaded VAE model", name="VAE")],
]:
    """Load a checkpoint file and extract its components.

    Returns:
        tuple: The model, CLIP, and VAE components
    """
    # Mock implementation
    return "model", "clip", "vae"


@pui.node(name="Save Image")
def save_image(
    images = NodeInput(python_type=str, description="Images to save"),
    filename_prefix = TextParameter(description="Prefix for saved image filenames", default="ComfyUI"),
) -> None:
    """Save images to disk with the specified filename prefix."""
    pass


# VAE Decode node
@pui.node(name="VAE Decode")
def vae_decode(
    samples = NodeInput(python_type=str, description="Samples to decode"),
    vae = NodeInput(python_type=str, description="VAE model to use for decoding"),
) -> Annotated[str, NodeOutput(description="Decoded image", name="IMAGE")]:
    """Decode latent samples using a VAE model."""
    return "decoded_image"


# Empty Latent Image node
@pui.node(name="Empty Latent Image")
def empty_latent_image(
    width = NumberParameter(default=512, description="Width of the latent image", min=64, max=2048),
    height = NumberParameter(default=512, description="Height of the latent image", min=64, max=2048),
    batch_size = NumberParameter(default=1, description="Batch size for generation", min=1, max=64),
) -> Annotated[str, NodeOutput(description="Empty latent image", name="LATENT")]:
    """Create an empty latent image with specified dimensions."""
    return "empty_latent"


# CLIP Text Encode node
@pui.node(name="CLIP Text Encode (Prompt)")
def clip_text_encode(
    clip = NodeInput(python_type=str, description="CLIP model to use for encoding"),
    text = TextParameter(
        default="beautiful scenery nature glass bottle landscape, , purple galaxy bottle,",
        description="Text prompt to encode",
    ),
) -> Annotated[str, NodeOutput(description="Encoded conditioning", name="CONDITIONING")]:
    """Encode text prompt using CLIP model."""
    return "encoded_text"


class Node(Enum):
    LOAD_CHECKPOINT = "Load Checkpoint"
    CLIP_TEXT_ENCODE = "CLIP Text Encode (Prompt)"
    VAE_DECODE = "VAE Decode"
    EMPTY_LATENT_IMAGE = "Empty Latent Image"
    K_SAMPLER = "KSampler" # for example we should be able to catch if wrong if not found
    SAVE_IMAGE = "Save Image"

positions = [
    NodePosition(x=-1588, y=427, node=Node.LOAD_CHECKPOINT),
    NodePosition(x=-1116, y=598, node=Node.CLIP_TEXT_ENCODE, index=0),
    NodePosition(x=-1072, y=-4, node=Node.CLIP_TEXT_ENCODE, index=1),
    NodePosition(x=-1010, y=868, node=Node.EMPTY_LATENT_IMAGE),
    NodePosition(x=-194, y=114, node=Node.K_SAMPLER),
    NodePosition(x=488, y=324, node=Node.VAE_DECODE),
    NodePosition(x=1078, y=326, node=Node.SAVE_IMAGE),
]

# edges = [
#       {
#         "source": {
#           "node": Node.LOAD_CHECKPOINT,
#           "output": "model",
#         },
#         "target": {
#           "node": Node.K_SAMPLER,
#           "input": "model",
#         }
#       },
#       {
#         "source": {
#           "node": Node.LOAD_CHECKPOINT,
#           "output": "clip",
#         },
#         "target": {
#           "node": Node.CLIP_TEXT_ENCODE,
#           "input": "clip",
#           "index": 0,
#         }
#       },
#       {
#         "source": {
#           "node": Node.LOAD_CHECKPOINT,
#           "output": "clip",
#         },
#         "target": {
#           "node": Node.CLIP_TEXT_ENCODE,
#           "input": "clip",
#           "index": 1,
#         }
#       },
#       {
#         "source": {
#           "node": Node.LOAD_CHECKPOINT,
#           "output": "vae",
#         },
#         "target": {
#           "node": Node.VAE_DECODE,
#           "input": "vae",
#           "index": 1,
#         }
#       },
#       {
#         "source": {
#           "node": Node.CLIP_TEXT_ENCODE,
#           "output": "conditioning",
#           "index": 0,
#         },
#         "target": {
#           "node": Node.K_SAMPLER,
#           "input": "positive",
#         }
#       },
#       {
#         "source": {
#           "node": Node.CLIP_TEXT_ENCODE,
#           "output": "conditioning",
#           "index": 1,
#         },
#         "target": {
#           "node": Node.K_SAMPLER,
#           "input": "negative",
#         }
#       },
#       {
#         "source": {
#           "node": Node.EMPTY_LATENT_IMAGE,
#           "output": "latent",
#         },
#         "target": {
#           "node": Node.K_SAMPLER,
#           "input": "latent_image",
#         }
#       },
#       {
#         "source": {
#           "node": Node.K_SAMPLER,
#           "output": "latent",
#         },
#         "target": {
#           "node": Node.VAE_DECODE,
#           "input": "samples",
#         }
#       },
#       {
#         "source": {
#           "node": Node.VAE_DECODE,
#           "output": "image",
#         },
#         "target": {
#           "node": Node.SAVE_IMAGE,
#           "input": "images",
#         }
#     },
# ]

# save everythign that is not default
non_default_values = {
    Node.CLIP_TEXT_ENCODE: {
        0: {"text": "beautiful scenery nature glass bottle landscape, , purple galaxy bottle,"},
        1: {"text": "text, watermark"},
    },
    Node.LOAD_CHECKPOINT: {
        0: {"model": "v1-5-pruned-emaonly.ckpt"},
    },
}

@pui.workflow(name="Complex Workflow", positions=positions)
def complex_workflow(
    model = TextParameter(description="Model to use for generation", default="v1-5-pruned-emaonly.ckpt"),
    positive_conditioning_text = TextParameter(description="Positive conditioning text", default="beautiful scenery nature glass bottle landscape, , purple galaxy bottle,"),
):
    # Load checkpoint
    model, clip, vae = load_checkpoint(model)

    # Encode positive prompt
    positive_conditioning = clip_text_encode(clip=clip, text=positive_conditioning_text)

    # Encode negative prompt
    negative_conditioning = clip_text_encode(clip=clip, text="text, watermark")

    # Create empty latent image
    latent = empty_latent_image()

    # Run sampling
    sampled = k_sampler(
        model=model,
        positive=positive_conditioning,
        negative=negative_conditioning,
        latent_image=latent,
    )

    # Decode the latent image
    decoded = vae_decode(samples=sampled, vae=vae)

    # Save the final image
    save_image(images=decoded)

    return decoded

    # this should return non_default_values

pui.start()