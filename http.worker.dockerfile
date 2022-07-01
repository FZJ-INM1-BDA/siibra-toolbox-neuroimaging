FROM python:3.10-slim
RUN pip install -U pip

RUN mkdir /requirements
COPY ./http_wrapper/requirements-worker.txt /requirements/
RUN pip install -r /requirements/requirements-worker.txt

COPY . /siibra_toolbox
WORKDIR /siibra_toolbox

RUN pip install .

WORKDIR /siibra_toolbox
USER nobody

ENTRYPOINT celery -A http_wrapper.scheduling.worker.app  worker -l INFO
