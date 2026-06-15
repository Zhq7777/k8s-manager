"""Pod service business logic"""

import logging
from typing import List, Optional
from datetime import datetime
from app.services.k8s_client import K8sClient
from app import schemas

logger = logging.getLogger(__name__)


class PodService:
    """Pod service"""

    def __init__(self, k8s_client: K8sClient):
        self.client = k8s_client

    def list_pods(self, namespace: str = "default") -> List[schemas.PodList]:
        """List pods in namespace"""
        try:
            pods = self.client.list_pods(namespace)
            result = []
            for pod in pods:
                status = pod.status.phase
                ready = self._get_ready_containers(pod)
                restarts = self._get_total_restarts(pod)
                age = self._calculate_age(pod.metadata.creation_timestamp)
                ip = pod.status.pod_ip

                result.append(
                    schemas.PodList(
                        name=pod.metadata.name,
                        namespace=pod.metadata.namespace,
                        status=status,
                        ready=ready,
                        restarts=restarts,
                        age=age,
                        ip=ip,
                    )
                )
            return result
        except Exception as e:
            logger.error(f"Failed to list pods: {e}")
            raise

    def get_pod_detail(self, name: str, namespace: str = "default") -> schemas.PodDetail:
        """Get pod details"""
        try:
            pod = self.client.get_pod(name, namespace)

            metadata = schemas.PodMetadata(
                name=pod.metadata.name,
                namespace=pod.metadata.namespace,
                labels=pod.metadata.labels or {},
                annotations=pod.metadata.annotations or {},
            )

            status = schemas.PodStatus(
                phase=pod.status.phase,
                ready=len([c for c in pod.status.conditions if c.type == "Ready" and c.status == "True"]) if pod.status.conditions else 0,
                total=len(pod.spec.containers),
                restarts=self._get_total_restarts(pod),
            )

            containers = []
            for i, container in enumerate(pod.spec.containers):
                if pod.status.container_statuses and i < len(pod.status.container_statuses):
                    container_status = pod.status.container_statuses[i]
                    ready = container_status.ready
                    restarts = container_status.restart_count
                    state = self._get_container_state(container_status)
                else:
                    ready = False
                    restarts = 0
                    state = "Unknown"

                containers.append(
                    schemas.PodContainer(
                        name=container.name,
                        image=container.image,
                        ready=ready,
                        restarts=restarts,
                        state=state,
                    )
                )

            return schemas.PodDetail(
                metadata=metadata,
                status=status,
                containers=containers,
                created_at=pod.metadata.creation_timestamp.isoformat(),
                node=pod.spec.node_name,
            )
        except Exception as e:
            logger.error(f"Failed to get pod details: {e}")
            raise

    def get_pod_logs(self, name: str, namespace: str = "default", container: Optional[str] = None):
        """Get pod logs"""
        try:
            logs = self.client.get_pod_logs(name, namespace, container)
            return logs
        except Exception as e:
            logger.error(f"Failed to get pod logs: {e}")
            raise

    def delete_pod(self, name: str, namespace: str = "default") -> bool:
        """Delete pod"""
        try:
            return self.client.delete_pod(name, namespace)
        except Exception as e:
            logger.error(f"Failed to delete pod: {e}")
            raise

    @staticmethod
    def _get_ready_containers(pod) -> str:
        """Get ready containers count"""
        if pod.status.container_statuses:
            ready = sum(1 for c in pod.status.container_statuses if c.ready)
            total = len(pod.status.container_statuses)
            return f"{ready}/{total}"
        return "0/0"

    @staticmethod
    def _get_total_restarts(pod) -> int:
        """Get total restarts"""
        if pod.status.container_statuses:
            return sum(c.restart_count for c in pod.status.container_statuses)
        return 0

    @staticmethod
    def _get_container_state(container_status) -> str:
        """Get container state"""
        if container_status.state.running:
            return "Running"
        elif container_status.state.waiting:
            return "Waiting"
        elif container_status.state.terminated:
            return "Terminated"
        return "Unknown"

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
