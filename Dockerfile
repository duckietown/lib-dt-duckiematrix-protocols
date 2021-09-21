FROM python:3.7

WORKDIR /dt_duckiematrix_protocols
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN find .

ENV DISABLE_CONTRACTS=1

RUN pipdeptree
RUN python setup.py develop --no-deps
