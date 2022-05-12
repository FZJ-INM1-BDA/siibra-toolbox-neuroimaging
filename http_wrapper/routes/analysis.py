from enum import Enum
from typing import Union
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, Field

from scheduling.worker import worker_analysis
from logger import logger

router = APIRouter()

# Request body model
# This allows FastAPI to generate openapi schema for the request
# for more detail, see fastapi doc: https://fastapi.tiangolo.com/tutorial/body/
class PostRequestModel(BaseModel):
    str_input: str
    float_input: float = Field(0.2, alias="float-input")
    int_input: int = 3
    class Config:
        allow_population_by_field_name = True

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
def post_analysis(post_body: PostRequestModel):
    res = worker_analysis.delay(**post_body.dict())
    return PostResponseModel(poll_url=res.id)

@router.get("/analysis/{analysis_id}", response_model=ResultModel)
def get_analysis(analysis_id):
    res = worker_analysis.AsyncResult(analysis_id)
    
    if res.state == ResultStatus.FAILURE.value:
        traceback=res.traceback
        res.forget()
        return ResultModelFailure(
            status=ResultStatus.FAILURE,
            traceback=traceback,
        )
    if res.state == ResultStatus.SUCCESS.value:
        result = res.get()
        res.forget()
        return ResultModelSuccess(
            status=ResultStatus.SUCCESS,
            result=result,
        )
    return ResultModelPending(
        status=res.state
    )