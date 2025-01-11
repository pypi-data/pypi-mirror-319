from typing import Annotated

from pipeline_ui import PipelineUI
from pipeline_ui.modules.node.schema.client.schema import NodeInput, NodeOutput

pui = PipelineUI()


@pui.node()
def add_numbers(
    a: Annotated[int, NodeInput(description="First number to add")],
    b: Annotated[int, NodeInput(description="Second number to add")],
) -> Annotated[int, NodeOutput(name="out1", description="Sum of the two numbers")]:
    return a + b


@pui.node()
def subtract_numbers(
    a: Annotated[int, NodeInput(description="Number to subtract from")],
    b: Annotated[int, NodeInput(description="Number to subtract")],
) -> Annotated[int, NodeOutput(name="out1", description="Result of subtraction")]:
    return a - b


@pui.node()
def get_number_twice(
    a: Annotated[int, NodeInput(description="Input number")],
) -> tuple[
    Annotated[int, NodeOutput(name="result", description="Original number")],
    Annotated[int, NodeOutput(name="double", description="Double the number")],
]:
    return a, a * 2


@pui.node()
def input_node(
    a: Annotated[int, NodeInput(description="Input value")],
) -> Annotated[int, NodeOutput(name="output", description="Output value")]:
    return a


@pui.workflow()
def example_workflow(x: int, y: int):
    """
    {
        "name": "example_workflow",
        "inputs": [
            {
                "name": "x",
                "type": "int",
                "to": "get_number_twice",
                "input_index": 0

            },
            {
                "name": "y",
                "type": "int",
                "to": "add_numbers",
                "input_index": 1
            }
        ],
        "edges": [
            {
                "from": {
                    "node": "get_number_twice",
                    "output_index": 0
                },
                "to": {
                    "node": "add_numbers",
                    "input_index": 0
                }
            },
            {
                "from": {
                    "node": "get_number_twice",
                    "output_index": 1
                },
                "to": {
                    "node": "add_numbers",
                    "input_index": 1
                }
            }
        ],
        "outputs": [
            {
                "name": "c",
                "type": "int",
                "from": "add_numbers",
                "input_index": 0
            }
        ]
    }
    """
    a, b = get_number_twice(x)
    c = add_numbers(a, b)
    return c


def example_workflow_simple(x: int, y: int):
    a, b = get_number_twice(x)
    c = add_numbers(a, b)
    return c


print("h2")

pui.start()
