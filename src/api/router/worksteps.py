"""
Workstep endpoints
"""

from fastapi import APIRouter, Depends, status, Body, Path
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse, Response
from starlette.requests import Request
from uuid import UUID

from src.authentication.auth import get_user_info
from src.database.database import get_db
from src.service.worksteps import (
    serv_get_worksteps_by_receipt,
    serv_update_workstep,
    serv_delete_workstep,
    serv_create_workstep,
    serv_get_workstep_by_id,
)

from src.api.models.worksteps import (WorkstepCreate,
                                      WorkstepUpdate,
                                      WorkstepResponse)

router = APIRouter(prefix="/api",
                   dependencies=[Depends(get_user_info)])


@router.post(
    "/worksteps",
    tags=["worksteps"],
    response_class=JSONResponse,
    response_model=WorkstepResponse,
    description="Endpoint to create a workstep",
    status_code=status.HTTP_201_CREATED,
    deprecated=False,
)
def endp_create_workstep(request: Request,
                         db_session: Session = Depends(get_db),
                         body: WorkstepCreate = Body(alias='workstepCreate',
                                                     title='Workstep Create Model')):
    """
    # POST Endpoint to create workstep

    :param request: General request information
    :param body: API post model
    :param db_session: database session
    :return: API response model
    """
    return serv_create_workstep(request=request, db_session=db_session, body=body)


@router.get(
    "/receipts/{receipt_id}/worksteps",
    tags=["worksteps"],
    response_class=JSONResponse,
    response_model=WorkstepResponse,
    description="Endpoint to get worksteps by receipt",
    status_code=status.HTTP_200_OK,
    deprecated=False,
)
def endp_get_worksteps_by_receipt(request: Request,
                                  db_session: Session = Depends(get_db),
                                  receipt_id: UUID = Path(alias='receipt_id',
                                                          title='UUID of receipt')):
    """
    # GET Endpoint to request all worksteps of a receipt


    :param request: General request information
    :param db_session: database session
    :param receipt_id: UUID of receipt
    :return: API response model
    """
    return serv_get_worksteps_by_receipt(request=request, db_session=db_session, receipt_id=receipt_id)


@router.get(
    "/worksteps/{uuid}",
    tags=["worksteps"],
    response_class=JSONResponse,
    response_model=WorkstepResponse,
    description="Endpoint to get a workstep by id",
    status_code=status.HTTP_200_OK,
    deprecated=False,
)
def endp_get_workstep_by_id(request: Request,
                            db_session: Session = Depends(get_db),
                            uuid: UUID = Path(alias='uuid',
                                              title='UUID of workstep')):
    """
    # GET Endpoint to request a workstep by id

    :param uuid: UUID of workstep
    :param request: General request information
    :param db_session: database session
    :return: API response model
    """
    return serv_get_workstep_by_id(request=request, db_session=db_session, uuid=uuid)


@router.patch(
    "/worksteps/{uuid}",
    tags=["worksteps"],
    response_class=JSONResponse,
    response_model=WorkstepResponse,
    description="Endpoint to update Workstep",
    status_code=status.HTTP_200_OK,
    deprecated=False,
)
def endp_update_workstep(request: Request,
                         db_session: Session = Depends(get_db),
                         uuid: UUID = Path(alias='uuid',
                                           title='UUID of workstep'),
                         body: WorkstepUpdate = Body(alias='workstepUpdate',
                                                     title='Workstep Patch Model')):
    """
    # PATCH Endpoint to update an existing workstep

    :param uuid: UUID of workstep
    :param request: General request information
    :param db_session: database session
    :param body: API patch model
    :return: API response model
    """
    return serv_update_workstep(request=request, db_session=db_session, uuid=uuid, body=body)


@router.delete(
    "/worksteps/{uuid}",
    tags=["worksteps"],
    response_class=Response,
    description="Endpoint to delete a workstep",
    status_code=status.HTTP_204_NO_CONTENT,
    deprecated=False,
)
def endp_delete_workstep(request: Request,
                         db_session: Session = Depends(get_db),
                         uuid: UUID = Path(alias='uuid',
                                           title='UUID of workstep')):
    """
    # DELETE Endpoint to remove workstep

    :param uuid: UUID of workstep
    :param request: General request information
    :param db_session: database session
    :return: API response model
    """
    return serv_delete_workstep(request=request, db_session=db_session, uuid=uuid)
