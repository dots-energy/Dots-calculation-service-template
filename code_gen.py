
from dots_infrastructure.code_gen.code_gen import CodeGenerator

code_generator = CodeGenerator("output")
with open("input.json", "r") as input_file:
    input_data = input_file.read()

code_generator.code_gen(input=input_data, code_output_dir="src", documentation_ouput_dir="documentation")