"""Data schemas"""

from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Dict, Any, List


class PodStatus(BaseModel):
    """Pod status information"""
    phase: str
    ready: int
    total: int
    restarts: int


class PodContainer(BaseModel):
    """Pod container information"""
    name: str
    image: str
    ready: bool
    restarts: int
    state: str


class PodMetadata(BaseModel):
    """Pod metadata"""
    name: str
    namespace: str
    labels: Dict[str, str]
    annotations: Dict[str, str]


class PodList(BaseModel):
    """Pod list item"""
    name: str
    namespace: str
    status: str
    ready: str
    restarts: int
    age: str
    ip: Optional[str] = None


class PodDetail(BaseModel):
    """Pod detailed information"""
    metadata: PodMetadata
    status: PodStatus
    containers: List[PodContainer]
    created_at: str
    node: Optional[str] = None


class DeploymentStatus(BaseModel):
    """Deployment status"""
    desired: int
    ready: int
    updated: int
    available: int


class DeploymentList(BaseModel):
    """Deployment list item"""
    name: str
    namespace: str
    ready: str
    up_to_date: int
    available: int
    age: str
    image: str


class DeploymentCreate(BaseModel):
    """Create deployment request"""
    name: str
    namespace: str = "default"
    image: str
    replicas: int = 1
    labels: Optional[Dict[str, str]] = None
    env: Optional[Dict[str, str]] = None


class Response(BaseModel):
    """Unified response format"""
    code: int = 200
    message: str = "success"
    data: Optional[Any] = None
