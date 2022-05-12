FROM python:3.10-slim
RUN pip install -U pip

COPY . /siibra_toolbox
WORKDIR /siibra_toolbox
RUN pip install -r ./http_wrapper/requirements-worker.txt

RUN pip install .

WORKDIR /siibra_toolbox/http_wrapper
USER nobody

ENTRYPOINT celery -A scheduling.worker.app  worker -l INFO
