# from pipeline_ui.modules.decorators.node.decorator import node
# from pipeline_ui.modules.decorators.workflow.decorator import workflow, workflows


# @node()
# def test_add(a: int, b: int) -> int:
#     return a + b


# @node()
# def test_multiply(a: int, b: int) -> int:
#     return a * b


# @workflow()
# def test_workflow(x: int, y: int):
#     a = test_add(x, y)
#     b = test_multiply(a, y)
#     return b


# def test_workflow_decorator():
#     # Check if the workflow was added to the workflows list
#     assert any(w["name"] == "test_workflow" for w in workflows)

#     # Find the test_workflow in the workflows list
#     test_workflow_info = next(w for w in workflows if w["name"] == "test_workflow")

#     # Check if the nodes are correctly identified
#     assert set(test_workflow_info["nodes"]) == {"test_add", "test_multiply"}

#     # Check if the edges are correctly identified
#     expected_edges = [
#         {
#             "from": {"node": "test_add", "output_index": 0},
#             "to": {"node": "test_multiply", "input_index": 0},
#         },
#     ]
#     assert test_workflow_info["edges"] == expected_edges


# def test_workflow_execution():
#     result = test_workflow(2, 3)
#     assert result == 15  # (2 + 3) * 3 = 15
