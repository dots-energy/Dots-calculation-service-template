
from dots_infrastructure.code_gen.code_gen import CodeGenerator
import json
import os

code_generator = CodeGenerator()
with open("input.json", "r") as input_file:
    input_data = input_file.read()

parsed_input_data = json.loads(input_data)
cs_name = code_generator.camel_case(parsed_input_data["name"])
cs_python_name = code_generator.get_python_filename(cs_name)

if os.path.exists("src/ExampleCalculationService"):
    os.rename("src/ExampleCalculationService", f"src/{cs_name}")

if os.path.exists(f"src/{cs_name}/calculation_service_test.py"):
    os.rename(f"src/{cs_name}/calculation_service_test.py", f"src/{cs_name}/{cs_python_name}.py")

if os.path.exists("test/test_template.py"):
    os.rename("test/test_template.py", f"test/test_{cs_python_name}.py")

code_generator.code_gen(input=input_data, code_output_dir=f"src/{cs_name}", documentation_ouput_dir="docs")

with open('pyproject.toml', 'r') as file:
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('ExampleCalculationService', cs_name)

# Write the file out again
with open('pyproject.toml', 'w') as file:
  file.write(filedata)