import os
import logging

CHANNEL = os.getenv("SIIBRA_TOOLBOX_NAME", "siibra_toolbox_neuroimaging")

logger = logging.getLogger(__name__)

try:
    from celery import Celery
except ImportError as e:
    logger.critical(f"Importing celery error")
    raise e

default_config="http_wrapper.conf.celeryconfig"
app = Celery(CHANNEL)
app.config_from_object(default_config)

@app.task(bind=True)
def worker_analysis(self, nii_filename: str) -> int:

    # It is imperative that we do not import heavy packages at root level
    # Since worker.py needs to be imported by server, it should have as little top level dependency as possible
    # Otherwise, ImportError will result.

    from siibra_toolbox_neuroimaging import AnatomicalAssignment
    from http_wrapper.util import get_task_inputdir, get_task_outputdir

    task_id = self.request.id
    task_input_dir = get_task_inputdir(task_id)
    task_output_dir = get_task_outputdir(task_id)

    path_to_nii = os.path.join(task_input_dir, nii_filename)
    
    logger.info(f"processing nifti file at {path_to_nii}")
    assignment = AnatomicalAssignment()
    assignments, component_mask = assignment.analyze(path_to_nii)
    logger.info(f"creating report")
    assignment.create_report(assignments, nii_filename, component_mask, outdir=task_output_dir)
    return 0

