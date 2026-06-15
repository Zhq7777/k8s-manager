"""Deployment service business logic"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
from kubernetes import client
from app.services.k8s_client import K8sClient
from app import schemas

logger = logging.getLogger(__name__)


class DeploymentService:
    """Deployment service"""

    def __init__(self, k8s_client: K8sClient):
        self.client = k8s_client

    def list_deployments(self, namespace: str = "default") -> List[schemas.DeploymentList]:
        """List deployments in namespace"""
        try:
            deployments = self.client.list_deployments(namespace)
            result = []
            for dep in deployments:
                image = ""
                if dep.spec.template.spec.containers:
                    image = dep.spec.template.spec.containers[0].image

                age = self._calculate_age(dep.metadata.creation_timestamp)
                ready = f"{dep.status.ready_replicas or 0}/{dep.status.desired_replicas or 0}"

                result.append(
                    schemas.DeploymentList(
                        name=dep.metadata.name,
                        namespace=dep.metadata.namespace,
                        ready=ready,
                        up_to_date=dep.status.updated_replicas or 0,
                        available=dep.status.available_replicas or 0,
                        age=age,
                        image=image,
                    )
                )
            return result
        except Exception as e:
            logger.error(f"Failed to list deployments: {e}")
            raise

    def get_deployment_detail(self, name: str, namespace: str = "default") -> schemas.DeploymentDetail:
        """Get deployment details"""
        try:
            dep = self.client.get_deployment(name, namespace)

            status = schemas.DeploymentStatus(
                desired=dep.status.desired_replicas or 0,
                ready=dep.status.ready_replicas or 0,
                updated=dep.status.updated_replicas or 0,
                available=dep.status.available_replicas or 0,
            )

            return schemas.DeploymentDetail(
                name=dep.metadata.name,
                namespace=dep.metadata.namespace,
                status=status,
                replicas=dep.spec.replicas,
                selector=dep.spec.selector.match_labels or {},
                created_at=dep.metadata.creation_timestamp.isoformat(),
            )
        except Exception as e:
            logger.error(f"Failed to get deployment details: {e}")
            raise

    def create_deployment(self, request: schemas.DeploymentCreate) -> Dict[str, Any]:
        """Create deployment"""
        try:
            env_vars = []
            if request.env:
                for key, value in request.env.items():
                    env_vars.append(client.V1EnvVar(name=key, value=value))

            container = client.V1Container(
                name=request.name,
                image=request.image,
                env=env_vars or None,
            )

            labels = request.labels or {"app": request.name}
            template_spec = client.V1PodTemplateSpec(
                metadata=client.V1ObjectMeta(labels=labels),
                spec=client.V1PodSpec(containers=[container]),
            )

            deployment = client.V1Deployment(
                api_version="apps/v1",
                kind="Deployment",
                metadata=client.V1ObjectMeta(name=request.name),
                spec=client.V1DeploymentSpec(
                    replicas=request.replicas,
                    selector=client.V1LabelSelector(match_labels=labels),
                    template=template_spec,
                ),
            )

            result = self.client.create_deployment(deployment.to_dict(), request.namespace)
            logger.info(f"Created deployment: {request.name}")
            return {"name": result.metadata.name, "namespace": result.metadata.namespace}
        except Exception as e:
            logger.error(f"Failed to create deployment: {e}")
            raise

    def update_deployment(self, name: str, request: schemas.DeploymentCreate, namespace: str = "default") -> Dict[str, Any]:
        """Update deployment"""
        try:
            dep = self.client.get_deployment(name, namespace)

            if request.image:
                for container in dep.spec.template.spec.containers:
                    container.image = request.image

            if request.replicas is not None:
                dep.spec.replicas = request.replicas

            if request.env:
                env_vars = [client.V1EnvVar(name=k, value=v) for k, v in request.env.items()]
                for container in dep.spec.template.spec.containers:
                    container.env = env_vars

            result = self.client.update_deployment(name, dep.to_dict(), namespace)
            logger.info(f"Updated deployment: {name}")
            return {"name": result.metadata.name, "namespace": result.metadata.namespace}
        except Exception as e:
            logger.error(f"Failed to update deployment: {e}")
            raise

    def delete_deployment(self, name: str, namespace: str = "default") -> bool:
        """Delete deployment"""
        try:
            return self.client.delete_deployment(name, namespace)
        except Exception as e:
            logger.error(f"Failed to delete deployment: {e}")
            raise

    def scale_deployment(self, name: str, replicas: int, namespace: str = "default") -> Dict[str, Any]:
        """Scale deployment"""
        try:
            dep = self.client.get_deployment(name, namespace)
            dep.spec.replicas = replicas
            result = self.client.update_deployment(name, dep.to_dict(), namespace)
            logger.info(f"Scaled deployment: {name} to {replicas} replicas")
            return {"name": result.metadata.name, "namespace": result.metadata.namespace, "replicas": replicas}
        except Exception as e:
            logger.error(f"Failed to scale deployment: {e}")
            raise

    @staticmethod
    def _calculate_age(creation_timestamp) -> str:
        """Calculate resource age"""
        if not creation_timestamp:
            return "Unknown"

        now = datetime.utcnow().replace(tzinfo=creation_timestamp.tzinfo)
        age = now - creation_timestamp
        seconds = age.total_seconds()

        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            return f"{int(seconds // 60)}m"
        elif seconds < 86400:
            return f"{int(seconds // 3600)}h"
        else:
            return f"{int(seconds // 86400)}d"
