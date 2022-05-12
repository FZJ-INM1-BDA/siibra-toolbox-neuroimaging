import os
import logging

CHANNEL = os.getenv("SIIBRA_TOOLBOX_NAME", "siibra_toolbox_template")

logger = logging.getLogger(__name__)

try:
    from celery import Celery
except ImportError as e:
    logger.critical(f"Importing celery error")
    raise e

default_config="conf.celeryconfig"
app = Celery(CHANNEL)
app.config_from_object(default_config)

@app.task
def worker_analysis(str_input: str, float_input: float, int_input: int) -> int:

    # It is imperative that we do not import heavy packages at root level
    # Since worker.py needs to be imported by server, it should have as little top level dependency as possible
    # Otherwise, ImportError will result.

    from siibra_toolbox_template import ToolboxTemplate
    instance = ToolboxTemplate()
    return instance.analysis(str_input, float_input, int_input)

