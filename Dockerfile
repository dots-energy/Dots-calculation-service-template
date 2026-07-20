FROM python:3.13

RUN mkdir /app/
WORKDIR /app

COPY src/Test src/Test
COPY pyproject.toml ./
COPY README.md ./
RUN pip install ./

ENTRYPOINT python3 src/Test/test.py