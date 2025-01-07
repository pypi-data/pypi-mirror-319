from typing import Dict, List, Union, Optional
from collections import OrderedDict
from typing_extensions import Annotated

from fastapi import APIRouter
from fastapi import Body
from fastapi import Path
from fastapi import Depends
from fastapi import status
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from ewoksutils import event_utils
from ewoksjob.client import submit
from ewoksjob.client import get_queues
from ewoksjob.client.local import submit as submit_local

from ...backends import json_backend
from ...config import EwoksSettingsType
from ..common import models as common_models
from ...models import EwoksSchedulingType
from . import models
from . import events

_base_execution_router = APIRouter()
v1_0_0_router = APIRouter()
v1_1_0_router = APIRouter()
v2_0_0_router = APIRouter()


@_base_execution_router.post(
    "/execute/{identifier}",
    summary="Execute workflow",
    response_model=models.EwoksJobInfo,
    response_description="Workflow execution job description",
    status_code=200,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "description": "No permission to read workflow",
            "model": common_models.ResourceIdentifierError,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Workflow not found",
            "model": common_models.ResourceIdentifierError,
        },
    },
)
def execute_workflow(
    settings: EwoksSettingsType,
    identifier: Annotated[
        str,
        Path(
            title="Workflow identifier",
            description="Unique identifier in the workflow database",
        ),
    ],
    options: Annotated[
        Optional[models.EwoksExecuteOptions], Body(title="Ewoks execute options")
    ] = None,
) -> Dict[str, Union[int, str]]:
    try:
        graph = json_backend.load_resource(
            settings.resource_directory / "workflows", identifier
        )
    except PermissionError:
        return JSONResponse(
            {
                "message": f"No permission to read workflow '{identifier}'.",
                "type": "workflow",
                "identifier": identifier,
            },
            status_code=status.HTTP_403_FORBIDDEN,
        )
    except FileNotFoundError:
        return JSONResponse(
            {
                "message": f"Workflow '{identifier}' is not found.",
                "type": "workflow",
                "identifier": identifier,
            },
            status_code=status.HTTP_404_NOT_FOUND,
        )

    if options is None:
        execute_arguments = None
        worker_options = None
    else:
        execute_arguments = options.execute_arguments
        worker_options = options.worker_options
    execute_arguments = json_backend.merge_mappings(
        graph["graph"].get("execute_arguments"), execute_arguments
    )
    submit_kwargs = json_backend.merge_mappings(
        graph["graph"].get("worker_options"), worker_options
    )

    # Workflow execution: position arguments
    submit_kwargs["args"] = (graph,)
    # Workflow execution: named arguments
    submit_kwargs["kwargs"] = execute_arguments

    execinfo = execute_arguments.setdefault("execinfo", dict())
    handlers = execinfo.setdefault("handlers", list())
    for handler in settings.ewoks_execution.handlers:
        if handler not in handlers:
            handlers.append(handler)

    if settings.ewoks_scheduling.type == EwoksSchedulingType.Local:
        future = submit_local(**submit_kwargs)
    else:
        future = submit(**submit_kwargs)
    return {"job_id": future.task_id}


v1_0_0_router.include_router(_base_execution_router)


@v1_0_0_router.get(
    "/execution/events",
    summary="Get workflow events",
    response_model=models.EwoksEventList_v1,
    response_description="Workflow execution jobs grouped per job ID",
    status_code=200,
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "Server not configured for ewoks events",
            "model": common_models.ResourceIdentifierError,
        },
    },
)
def execute_events_v1(
    settings: EwoksSettingsType,
    filters: Annotated[
        models.EwoksEventFilter, Depends(models.EwoksEventFilter)
    ],  # pydantic model to parse query parameters
) -> Dict[str, List[List[Dict]]]:
    jobs = OrderedDict()
    with events.reader_context(settings) as reader:
        if reader is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Server not configured for ewoks events",
            )
        for event in reader.get_events(**filters.model_dump(exclude_none=True)):
            job_id = event["job_id"]
            if job_id not in jobs:
                jobs[job_id] = list()
            if "engine" in event_utils.FIELD_TYPES:
                event["binding"] = event.pop("engine")
            jobs[job_id].append(event)
    return {"jobs": list(jobs.values())}


v1_1_0_router.include_router(v1_0_0_router)


@v1_1_0_router.get(
    "/execution/workers",
    summary="Get workers",
    response_model=models.EwoksWorkerList,
    response_description="List of available workers",
    status_code=200,
)
def workers(settings: EwoksSettingsType) -> Dict[str, Optional[List[str]]]:
    if settings.ewoks_scheduling.type == EwoksSchedulingType.Local:
        return {"workers": None}

    return {"workers": get_queues()}


v2_0_0_router.include_router(_base_execution_router)


@v2_0_0_router.get(
    "/execution/events",
    summary="Get workflow events",
    response_model=models.EwoksEventList_v2,
    response_description="Workflow execution jobs grouped per job ID",
    status_code=200,
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "Server not configured for ewoks events",
            "model": common_models.ResourceIdentifierError,
        },
    },
)
def execute_events_v2(
    settings: EwoksSettingsType,
    filters: Annotated[
        models.EwoksEventFilter, Depends(models.EwoksEventFilter)
    ],  # pydantic model to parse query parameters
) -> Dict[str, List[List[Dict]]]:
    jobs = OrderedDict()
    with events.reader_context(settings) as reader:
        if reader is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Server not configured for ewoks events",
            )
        for event in reader.get_events(**filters.model_dump(exclude_none=True)):
            job_id = event["job_id"]
            if job_id not in jobs:
                jobs[job_id] = list()
            jobs[job_id].append(event)
    return {"jobs": list(jobs.values())}


@v2_0_0_router.get(
    "/execution/queues",
    summary="Get queues",
    response_model=models.EwoksQueueList,
    response_description="List of available queues",
    status_code=200,
)
def queues(settings: EwoksSettingsType) -> Dict[str, Optional[List[str]]]:
    if settings.ewoks_scheduling.type == EwoksSchedulingType.Local:
        return {"queues": None}

    return {"queues": get_queues()}
