# from src.modules.parser.decorator_parser import transform_to_generator

# from pipeline_ui.modules.decorators.node.decorator import node
# from pipeline_ui.modules.decorators.workflow.decorator import workflow


# @node()
# def get_number_twice(x: int) -> tuple[int, int]:
#     return x, x


# @node()
# def add_numbers(a: int, b: int) -> int:
#     return a + b


# @workflow()
# def example_workflow_simple(x: int, y: int) -> int:
#     a, b = get_number_twice(x)
#     c = add_numbers(a, b)
#     return c


# def test_example_workflow_simple():
#     transformed_workflow = transform_to_generator(example_workflow_simple)
#     gen = transformed_workflow(5, 3)
#     output = list(gen)
#     assert output == [{"output": (5, 5)}, {"output": 10}, {"end": 10}]
#     print("Test passed. Output:", output)


# # Run the test
# test_example_workflow_simple()

# if __name__ == "__main__":
#     test_example_workflow_simple()
