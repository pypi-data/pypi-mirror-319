# from src.modules.parser.decorator_parser import transform_to_generator

# # def test_transform_to_generator():
# #     def example_function(x: int, y: int) -> int:
# #         a = x + 1
# #         b = y * 2
# #         c = a + b
# #         return c

# #     transformed_func = transform_to_generator(example_function)

# #     result = list(transformed_func(3, 4))

# #     assert len(result) == 4
# #     assert result[0] == {'output': 4}  # a = x + 1
# #     assert result[1] == {'output': 8}  # b = y * 2
# #     assert result[2] == {'output': 12}  # c = a + b
# #     assert result[3] == {'end': 12}  # return c

# #     # Test with different inputs
# #     result = list(transformed_func(5, 2))

# #     assert len(result) == 4
# #     assert result[0] == {'output': 6}  # a = x + 1
# #     assert result[1] == {'output': 4}  # b = y * 2
# #     assert result[2] == {'output': 10}  # c = a + b
# #     assert result[3] == {'end': 10}  # return c

# # def test_transform_to_generator_with_multiple_assignments():
# #     def multiple_assignments(x: int) -> tuple:
# #         a, b = x, x + 1
# #         c, d = b + 1, a * 2
# #         return a, b, c, d

# #     transformed_func = transform_to_generator(multiple_assignments)

# #     result = list(transformed_func(5))

# #     assert len(result) == 3
# #     assert result[0] == {'output': (5, 6)}  # a, b = x, x + 1
# #     assert result[1] == {'output': (7, 10)}  # c, d = b + 1, a * 2
# #     assert result[2] == {'end': (5, 6, 7, 10)}  # return a, b, c, d


# def test_transform_to_generator_example_workflow():
#     def get_number_twice(x: int) -> tuple[int, int]:
#         return x, x

#     def add_numbers(a: int, b: int) -> int:
#         return a + b

#     def example_workflow_simple(x: int, y: int) -> int:
#         a, b = get_number_twice(x)
#         c = add_numbers(a, b)
#         return c

#     transformed_workflow = transform_to_generator(example_workflow_simple)

#     # print(type(transformed_workflow(5, 3)))

#     for step in transformed_workflow(5, 3):
#         print("hello")
#         print(step)

#     result = list(transformed_workflow(5, 3))

#     assert len(result) == 3
#     assert result[0] == {"output": (5, 5)}  # a, b = get_number_twice(x)
#     assert result[1] == {"output": 10}  # c = add_numbers(a, b)
#     assert result[2] == {"end": 10}  # return c


# if __name__ == "__main__":
#     # pytest.main(["-v", __file__])
#     test_transform_to_generator_example_workflow()
