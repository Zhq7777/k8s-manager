"""Deployment API routes"""

from fastapi import APIRouter, HTTPException, status, Query
from app import schemas
from app.services.k8s_client import K8sClient
from app.services.deployment_service import DeploymentService

router = APIRouter(prefix="/deployments", tags=["deployments"])


@router.get("", response_model=schemas.Response)
async def list_deployments(namespace: str = Query("default")):
    """List deployments in namespace"""
    try:
        client = K8sClient()
        service = DeploymentService(client)
        deployments = service.list_deployments(namespace)
        return schemas.Response(
            code=200,
            message="success",
            data=[dep.model_dump() for dep in deployments],
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{deployment_name}", response_model=schemas.Response)
async def get_deployment(deployment_name: str, namespace: str = Query("default")):
    """Get deployment details"""
    try:
        client = K8sClient()
        service = DeploymentService(client)
        deployment = service.get_deployment_detail(deployment_name, namespace)
        return schemas.Response(
            code=200,
            message="success",
            data=deployment.model_dump(),
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("", response_model=schemas.Response)
async def create_deployment(request: schemas.DeploymentCreate):
    """Create deployment"""
    try:
        client = K8sClient()
        service = DeploymentService(client)
        result = service.create_deployment(request)
        return schemas.Response(
            code=200,
            message="success",
            data=result,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{deployment_name}", response_model=schemas.Response)
async def update_deployment(
    deployment_name: str,
    request: schemas.DeploymentCreate,
    namespace: str = Query("default"),
):
    """Update deployment"""
    try:
        client = K8sClient()
        service = DeploymentService(client)
        result = service.update_deployment(deployment_name, request, namespace)
        return schemas.Response(
            code=200,
            message="success",
            data=result,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{deployment_name}", response_model=schemas.Response)
async def delete_deployment(deployment_name: str, namespace: str = Query("default")):
    """Delete deployment"""
    try:
        client = K8sClient()
        service = DeploymentService(client)
        result = service.delete_deployment(deployment_name, namespace)
        return schemas.Response(
            code=200,
            message="success",
            data={"deleted": result},
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/{deployment_name}/scale", response_model=schemas.Response)
async def scale_deployment(
    deployment_name: str,
    replicas: int = Query(...),
    namespace: str = Query("default"),
):
    """Scale deployment"""
    try:
        client = K8sClient()
        service = DeploymentService(client)
        result = service.scale_deployment(deployment_name, replicas, namespace)
        return schemas.Response(
            code=200,
            message="success",
            data=result,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
