FROM python:3.9.0
# If needed you can use the official python image (larger memory size)
#FROM python:3.9.0

RUN mkdir /app/
WORKDIR /app

COPY src/<<INSERT_FOLDER_NAME>> src/<<INSERT_FOLDER_NAME>>
COPY pyproject.toml ./
COPY README.md ./
RUN pip install ./

ENTRYPOINT python3 src/<<INSERT_FOLDER_NAME>>/<<INSERT_IMPLEMENTATION_PYTHON_FILENAME>>.py