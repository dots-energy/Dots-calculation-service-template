
from dots_infrastructure.code_gen.code_gen import CodeGenerator
import json
import os

code_generator = CodeGenerator()
with open("input.json", "r") as input_file:
    input_data = input_file.read()

json.loads(input_data)
cs_name = input_data["name"]
cs_python_name = code_generator.get_python_filename(cs_name)

if os.path.exists("src/ExampleCalculationService"):
    os.rename("src/ExampleCalculationService", f"src/{cs_name}")

if os.path.exists(f"src/{cs_name}/calculation_service_test.py"):
    os.rename(f"src/{cs_name}/calculation_service_test.py", f"src/{cs_name}/{cs_python_name}.py")

if os.path.exists("test/test_template.py"):
    os.rename("test/test_template.py", f"test/test_{cs_python_name}.py")

code_generator.code_gen(input=input_data, code_output_dir=f"{cs_name}/src", documentation_ouput_dir="docs")