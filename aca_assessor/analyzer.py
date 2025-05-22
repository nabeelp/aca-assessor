"""
Analyzer module for ACA compatibility assessment.
"""
from typing import Dict, List, Any
from rich.console import Console
from rich.table import Table

console = Console()

class ACAAnalyzer:
    def __init__(self):
        # ACA limitations and constraints
        self.aca_constraints = {
            'max_memory': '16Gi',
            'max_cpu': '4',
            'supported_volume_types': ['secret', 'configmap'],
            'max_replicas': 30,
            'supported_protocols': ['TCP', 'HTTP', 'HTTPS']
        }

    def analyze_deployments(self, deployments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze deployments for ACA compatibility."""
        analysis_results = []
        
        for deployment in deployments:
            analysis = {
                'name': deployment['name'],
                'namespace': deployment['namespace'],
                'compatibility_issues': [],
                'recommendations': [],
                'compatibility_score': 100  # Start with perfect score and deduct based on issues
            }

            # Analyze each aspect
            self._analyze_resources(deployment, analysis)
            self._analyze_volumes(deployment, analysis)
            self._analyze_networking(deployment, analysis)
            self._analyze_scaling(deployment, analysis)

            # Calculate final score
            analysis['compatibility_score'] = max(0, analysis['compatibility_score'])
            analysis_results.append(analysis)

        return analysis_results

    def _analyze_resources(self, deployment: Dict[str, Any], analysis: Dict[str, Any]):
        """Analyze resource requirements."""
        for container in deployment['containers']:
            resources = container['resources']
            
            # Check CPU limits
            if 'limits' in resources and 'cpu' in resources['limits']:
                cpu_limit = self._convert_cpu_to_cores(resources['limits']['cpu'])
                if cpu_limit > 4:
                    analysis['compatibility_issues'].append(
                        f"Container '{container['name']}' CPU limit ({resources['limits']['cpu']}) exceeds ACA maximum (4 cores)"
                    )
                    analysis['recommendations'].append(
                        f"Reduce CPU limit for container '{container['name']}' to 4 cores or less"
                    )
                    analysis['compatibility_score'] -= 15

            # Check memory limits
            if 'limits' in resources and 'memory' in resources['limits']:
                memory_limit = self._convert_memory_to_gi(resources['limits']['memory'])
                if memory_limit > 16:
                    analysis['compatibility_issues'].append(
                        f"Container '{container['name']}' memory limit ({resources['limits']['memory']}) exceeds ACA maximum (16Gi)"
                    )
                    analysis['recommendations'].append(
                        f"Reduce memory limit for container '{container['name']}' to 16Gi or less"
                    )
                    analysis['compatibility_score'] -= 15

    def _analyze_volumes(self, deployment: Dict[str, Any], analysis: Dict[str, Any]):
        """Analyze volume configurations."""
        for volume in deployment['volumes']:
            if volume['type'] not in self.aca_constraints['supported_volume_types']:
                analysis['compatibility_issues'].append(
                    f"Volume type '{volume['type']}' is not supported in ACA"
                )
                analysis['recommendations'].append(
                    f"Consider using Azure Storage or other cloud storage solutions for persistent storage needs"
                )
                analysis['compatibility_score'] -= 10

    def _analyze_networking(self, deployment: Dict[str, Any], analysis: Dict[str, Any]):
        """Analyze networking configuration."""
        for container in deployment['containers']:
            for port in container['ports']:
                if port['protocol'] not in self.aca_constraints['supported_protocols']:
                    analysis['compatibility_issues'].append(
                        f"Protocol '{port['protocol']}' is not supported in ACA"
                    )
                    analysis['recommendations'].append(
                        f"Consider using HTTP/HTTPS or TCP for container '{container['name']}'"
                    )
                    analysis['compatibility_score'] -= 10

    def _analyze_scaling(self, deployment: Dict[str, Any], analysis: Dict[str, Any]):
        """Analyze scaling configuration."""
        if deployment['replicas'] > self.aca_constraints['max_replicas']:
            analysis['compatibility_issues'].append(
                f"Deployment replica count ({deployment['replicas']}) exceeds ACA maximum ({self.aca_constraints['max_replicas']})"
            )
            analysis['recommendations'].append(
                "Consider reducing max replicas or splitting the service"
            )
            analysis['compatibility_score'] -= 10

    def _convert_cpu_to_cores(self, cpu: str) -> float:
        """Convert CPU string to number of cores."""
        try:
            if cpu.endswith('m'):
                return float(cpu[:-1]) / 1000
            return float(cpu)
        except ValueError:
            return 0

    def _convert_memory_to_gi(self, memory: str) -> float:
        """Convert memory string to GiB."""
        try:
            num = float(''.join(filter(str.isdigit, memory)))
            unit = ''.join(filter(str.isalpha, memory)).lower()
            
            conversions = {
                'ki': num / (1024 * 1024),
                'mi': num / 1024,
                'gi': num,
                'ti': num * 1024,
                'k': num / (1000 * 1024),
                'm': num / 1024,
                'g': num,
                't': num * 1024
            }
            
            return conversions.get(unit, num)
        except ValueError:
            return 0

    def generate_report(self, analysis_results: List[Dict[str, Any]]):
        """Generate a formatted report of the analysis results."""
        table = Table(title="ACA Compatibility Assessment Report")
        
        table.add_column("Application", style="cyan")
        table.add_column("Compatibility Score", style="magenta")
        table.add_column("Issues", style="red")
        table.add_column("Recommendations", style="green")

        for result in analysis_results:
            table.add_row(
                f"{result['namespace']}/{result['name']}",
                f"{result['compatibility_score']}%",
                "\n".join(result['compatibility_issues']) or "No issues found",
                "\n".join(result['recommendations']) or "No recommendations"
            )

        console.print(table)
