"""
Kubernetes resource collector module for ACA Assessor.
"""
from typing import Dict, List, Any
from kubernetes import client, config
from rich.console import Console
from rich.table import Table

console = Console()

class KubernetesCollector:
    def __init__(self):
        try:
            config.load_kube_config()
            self.v1 = client.CoreV1Api()
            self.apps_v1 = client.AppsV1Api()
            self.networking_v1 = client.NetworkingV1Api()
            console.print("[green]Successfully connected to Kubernetes cluster[/green]")
        except Exception as e:
            console.print(f"[red]Failed to connect to Kubernetes cluster: {str(e)}[/red]")
            raise

    def collect_deployments(self, namespace: str = None) -> List[Dict[str, Any]]:
        """Collect all deployments in the specified namespace or all namespaces."""
        try:
            if namespace:
                deployments = self.apps_v1.list_namespaced_deployment(namespace)
            else:
                deployments = self.apps_v1.list_deployment_for_all_namespaces()
            
            return self._process_deployments(deployments.items)
        except Exception as e:
            console.print(f"[red]Error collecting deployments: {str(e)}[/red]")
            return []

    def _process_deployments(self, deployments: List[Any]) -> List[Dict[str, Any]]:
        """Process deployment information into a structured format."""
        processed = []
        for dep in deployments:
            containers = dep.spec.template.spec.containers
            processed.append({
                'name': dep.metadata.name,
                'namespace': dep.metadata.namespace,
                'replicas': dep.spec.replicas,
                'containers': [{
                    'name': c.name,
                    'image': c.image,
                    'resources': self._process_resources(c.resources),
                    'ports': self._process_ports(c.ports),
                    'env': self._process_env(c.env),
                    'volume_mounts': self._process_volume_mounts(c.volume_mounts)
                } for c in containers],
                'volumes': self._process_volumes(dep.spec.template.spec.volumes),
                'labels': dep.metadata.labels or {},
                'annotations': dep.metadata.annotations or {}
            })
        return processed

    def _process_resources(self, resources: Any) -> Dict[str, Dict[str, str]]:
        """Process container resource requirements."""
        if not resources:
            return {'requests': {}, 'limits': {}}
        
        return {
            'requests': {
                'cpu': resources.requests.get('cpu', ''),
                'memory': resources.requests.get('memory', '')
            } if resources.requests else {},
            'limits': {
                'cpu': resources.limits.get('cpu', ''),
                'memory': resources.limits.get('memory', '')
            } if resources.limits else {}
        }

    def _process_ports(self, ports: List[Any]) -> List[Dict[str, Any]]:
        """Process container port configurations."""
        if not ports:
            return []
        return [{
            'name': p.name,
            'container_port': p.container_port,
            'protocol': p.protocol
        } for p in ports]

    def _process_env(self, env: List[Any]) -> List[Dict[str, str]]:
        """Process container environment variables."""
        if not env:
            return []
        return [{
            'name': e.name,
            'value': e.value if e.value else 'FROM_SECRET' if e.value_from else ''
        } for e in env]

    def _process_volume_mounts(self, mounts: List[Any]) -> List[Dict[str, str]]:
        """Process container volume mounts."""
        if not mounts:
            return []
        return [{
            'name': m.name,
            'mount_path': m.mount_path,
            'read_only': m.read_only if hasattr(m, 'read_only') else False
        } for m in mounts]

    def _process_volumes(self, volumes: List[Any]) -> List[Dict[str, Any]]:
        """Process pod volumes."""
        if not volumes:
            return []
        processed = []
        for vol in volumes:
            vol_info = {'name': vol.name}
            if vol.persistent_volume_claim:
                vol_info['type'] = 'pvc'
                vol_info['claim_name'] = vol.persistent_volume_claim.claim_name
            elif vol.config_map:
                vol_info['type'] = 'configmap'
                vol_info['config_map_name'] = vol.config_map.name
            elif vol.secret:
                vol_info['type'] = 'secret'
                vol_info['secret_name'] = vol.secret.secret_name
            else:
                vol_info['type'] = 'other'
            processed.append(vol_info)
        return processed
