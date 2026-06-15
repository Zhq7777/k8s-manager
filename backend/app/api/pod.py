"""Pod API routes"""

from typing import Optional
from fastapi import APIRouter, HTTPException, status, Query
from app import schemas
from app.services.k8s_client import K8sClient
from app.services.pod_service import PodService

router = APIRouter(prefix="/pods", tags=["pods"])


@router.get("", response_model=schemas.Response)
async def list_pods(namespace: str = Query("default")):
    """List pods in namespace
    
    Query Parameters:
        namespace: Kubernetes namespace (default: "default")
    """
    try:
        client = K8sClient()
        service = PodService(client)
        pods = service.list_pods(namespace)
        return schemas.Response(
            code=200,
            message="success",
            data=[pod.model_dump() for pod in pods],
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{pod_name}", response_model=schemas.Response)
async def get_pod(pod_name: str, namespace: str = Query("default")):
    """Get pod details
    
    Path Parameters:
        pod_name: Pod name
    Query Parameters:
        namespace: Kubernetes namespace
    """
    try:
        client = K8sClient()
        service = PodService(client)
        pod = service.get_pod_detail(pod_name, namespace)
        return schemas.Response(
            code=200,
            message="success",
            data=pod.model_dump(),
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{pod_name}/logs", response_model=schemas.Response)
async def get_pod_logs(
    pod_name: str,
    namespace: str = Query("default"),
    container: Optional[str] = Query(None),
):
    """Get pod logs
    
    Path Parameters:
        pod_name: Pod name
    Query Parameters:
        namespace: Kubernetes namespace
        container: Container name (optional)
    """
    try:
        client = K8sClient()
        service = PodService(client)
        logs = service.get_pod_logs(pod_name, namespace, container)
        return schemas.Response(
            code=200,
            message="success",
            data={"logs": logs, "container": container or "default"},
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{pod_name}", response_model=schemas.Response)
async def delete_pod(pod_name: str, namespace: str = Query("default")):
    """Delete pod
    
    Path Parameters:
        pod_name: Pod name
    Query Parameters:
        namespace: Kubernetes namespace
    """
    try:
        client = K8sClient()
        service = PodService(client)
        result = service.delete_pod(pod_name, namespace)
        return schemas.Response(
            code=200,
            message="success",
            data={"deleted": result},
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
