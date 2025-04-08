FROM python:3.9.0
# If needed you can use the official python image (larger memory size)
#FROM python:3.9.0

RUN mkdir /app/
WORKDIR /app

COPY src/service_a src/service_a
COPY requirements.txt ./
COPY pyproject.toml ./
COPY README.md ./
RUN pip install -r requirements.txt
RUN pip install ./

ENTRYPOINT python3 src/service_a/service_a_calc.py