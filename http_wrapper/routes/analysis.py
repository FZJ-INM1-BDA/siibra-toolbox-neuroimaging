from enum import Enum
from typing import Union
from fastapi import APIRouter, UploadFile
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field
from celery import uuid
import os
import shutil

from http_wrapper.scheduling.worker import worker_analysis
from http_wrapper.logger import logger
from http_wrapper.util import get_task_inputdir, get_task_outputdir

router = APIRouter()

class PostResponseModel(BaseModel):
    poll_url: str


class ResultStatus(str, Enum):
    SUCCESS="SUCCESS"
    FAILURE="FAILURE"
    PENDING="PENDING"
    STARTED="STARTED"
    RETRY="RETRY"

class ResultBaseModel(BaseModel):
    status: ResultStatus
    class Config:
        use_enum_values: True

class ResultModelSuccess(ResultBaseModel):
    # This would be the result of the output of the analysis. In this case, it is an integer. If the result is more complex,
    # it should be described using pydantic.
    result: int

class ResultModelFailure(ResultBaseModel):
    traceback: str

class ResultModelPending(ResultBaseModel): pass

ResultModel = Union[ResultModelSuccess, ResultModelFailure, ResultModelPending]

@router.post("/analysis", response_model=PostResponseModel)
def post_analysis(nifti: UploadFile):
    task_id = uuid()
    task_inputdir = get_task_inputdir(task_id)

    path_to_nii = os.path.join(task_inputdir, nifti.filename)
    
    with open(path_to_nii, 'wb') as buffer:
        shutil.copyfileobj(nifti.file, buffer)
    
    logger.info(f"saved {nifti.filename} to {path_to_nii}")
    worker_analysis.apply_async([], {"nii_filename": path_to_nii}, task_id=task_id)
    return PostResponseModel(poll_url=task_id)

@router.get("/analysis/{analysis_id}", response_model=ResultModel)
def get_analysis(analysis_id:str):
    res = worker_analysis.AsyncResult(analysis_id)
    
    # TODO currently the tasks are not forgotten
    # it may lead to memleak (eventually)
    if res.state == ResultStatus.FAILURE.value:
        traceback=res.traceback
        return ResultModelFailure(
            status=ResultStatus.FAILURE,
            traceback=traceback,
        )
    if res.state == ResultStatus.SUCCESS.value:
        result = res.get()
        return ResultModelSuccess(
            status=ResultStatus.SUCCESS,
            result=result,
        )
    return ResultModelPending(
        status=res.state
    )

# TODO need to clean up the artefacts & uploads
@router.get("/analysis/{analysis_id}/download", response_class=FileResponse)
def get_analysis_zip(analysis_id:str):
    res = worker_analysis.AsyncResult(analysis_id)
    if res.state != ResultStatus.SUCCESS.value:
        raise HTTPException(
            status_code=404,
            detail=f"Result not found. Check if the analysis_id is correct. Or the result might not yet be ready."
        )
    
    task_output_dir = get_task_outputdir(analysis_id)
    
    import zipfile, io
    bytesio = io.BytesIO()
    
    target_files = [( f, dirpath)
        for dirpath, _dirnames, filenames in os.walk(task_output_dir)
        for f in filenames]
    with zipfile.ZipFile(bytesio, mode="w", compression=zipfile.ZIP_DEFLATED) as zip:
        for filename, dirpath in target_files:
            path_to_file = os.path.join(dirpath, filename)
            archive_filename = path_to_file.replace(task_output_dir, "")
            zip.write(path_to_file, archive_filename)
    return StreamingResponse(
        iter([bytesio.getvalue()]),
        media_type="application/x-zip-compressed",
        headers={
            "Content-Disposition": f"attachcment; filename={analysis_id}.zip"
        }
    )
            