"""Kubernetes client wrapper"""

import logging
from typing import Optional
from kubernetes import client, config
from kubernetes.client import ApiClient
from app.config import settings

logger = logging.getLogger(__name__)


class K8sClient:
    """Kubernetes client"""

    def __init__(self, kubeconfig_path: Optional[str] = None):
        """Initialize K8s client"""
        self.kubeconfig_path = kubeconfig_path or settings.KUBECONFIG_PATH
        self._api_client = None
        self._v1 = None
        self._apps_v1 = None

    def _init_client(self):
        """Initialize client connection"""
        if self._api_client is not None:
            return

        try:
            if settings.IN_CLUSTER:
                config.load_incluster_config()
                logger.info("Using in-cluster authentication")
            elif self.kubeconfig_path:
                config.load_kube_config(config_file=self.kubeconfig_path)
                logger.info(f"Loaded kubeconfig: {self.kubeconfig_path}")
            else:
                config.load_kube_config()
                logger.info("Using default kubeconfig")
        except Exception as e:
            logger.error(f"Failed to initialize K8s client: {e}")
            raise

        self._api_client = ApiClient()

    @property
    def v1(self) -> client.CoreV1Api:
        """Get Core API v1"""
        if self._v1 is None:
            self._init_client()
            self._v1 = client.CoreV1Api()
        return self._v1

    @property
    def apps_v1(self) -> client.AppsV1Api:
        """Get Apps API v1"""
        if self._apps_v1 is None:
            self._init_client()
            self._apps_v1 = client.AppsV1Api()
        return self._apps_v1

    def get_namespaces(self) -> list:
        """Get all namespaces"""
        try:
            namespaces = self.v1.list_namespace()
            return [ns.metadata.name for ns in namespaces.items]
        except Exception as e:
            logger.error(f"Failed to get namespaces: {e}")
            raise

    def list_pods(self, namespace: str = "default") -> list:
        """List pods in namespace"""
        try:
            pods = self.v1.list_namespaced_pod(namespace)
            return pods.items
        except Exception as e:
            logger.error(f"Failed to list pods: {e}")
            raise

    def get_pod(self, name: str, namespace: str = "default"):
        """Get pod details"""
        try:
            return self.v1.read_namespaced_pod(name, namespace)
        except Exception as e:
            logger.error(f"Failed to get pod: {e}")
            raise

    def delete_pod(self, name: str, namespace: str = "default") -> bool:
        """Delete pod"""
        try:
            self.v1.delete_namespaced_pod(name, namespace)
            logger.info(f"Deleted pod: {name}/{namespace}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete pod: {e}")
            raise

    def get_pod_logs(self, name: str, namespace: str = "default", container: Optional[str] = None) -> str:
        """Get pod logs"""
        try:
            logs = self.v1.read_namespaced_pod_log(
                name,
                namespace,
                container=container,
                tail_lines=500,
            )
            return logs
        except Exception as e:
            logger.error(f"Failed to get pod logs: {e}")
            raise

    def list_deployments(self, namespace: str = "default") -> list:
        """List deployments in namespace"""
        try:
            deployments = self.apps_v1.list_namespaced_deployment(namespace)
            return deployments.items
        except Exception as e:
            logger.error(f"Failed to list deployments: {e}")
            raise

    def get_deployment(self, name: str, namespace: str = "default"):
        """Get deployment details"""
        try:
            return self.apps_v1.read_namespaced_deployment(name, namespace)
        except Exception as e:
            logger.error(f"Failed to get deployment: {e}")
            raise

    def create_deployment(self, deployment_dict: dict, namespace: str = "default"):
        """Create deployment"""
        try:
            body = client.V1Deployment(**deployment_dict)
            result = self.apps_v1.create_namespaced_deployment(namespace, body)
            logger.info(f"Created deployment: {result.metadata.name}")
            return result
        except Exception as e:
            logger.error(f"Failed to create deployment: {e}")
            raise

    def update_deployment(self, name: str, deployment_dict: dict, namespace: str = "default"):
        """Update deployment"""
        try:
            body = client.V1Deployment(**deployment_dict)
            result = self.apps_v1.patch_namespaced_deployment(name, namespace, body)
            logger.info(f"Updated deployment: {name}")
            return result
        except Exception as e:
            logger.error(f"Failed to update deployment: {e}")
            raise

    def delete_deployment(self, name: str, namespace: str = "default") -> bool:
        """Delete deployment"""
        try:
            self.apps_v1.delete_namespaced_deployment(name, namespace)
            logger.info(f"Deleted deployment: {name}/{namespace}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete deployment: {e}")
            raise

    def list_services(self, namespace: str = "default") -> list:
        """List services in namespace"""
        try:
            services = self.v1.list_namespaced_service(namespace)
            return services.items
        except Exception as e:
            logger.error(f"Failed to list services: {e}")
            raise

    def get_service(self, name: str, namespace: str = "default"):
        """Get service details"""
        try:
            return self.v1.read_namespaced_service(name, namespace)
        except Exception as e:
            logger.error(f"Failed to get service: {e}")
            raise
