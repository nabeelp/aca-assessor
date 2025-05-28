"""
Command-line interface for ACA Assessor.
"""
import click
from rich.console import Console
from .collector import KubernetesCollector
from .analyzer import ACAAnalyzer

console = Console()

@click.group()
def cli():
    """ACA Assessor - Analyze Kubernetes applications for Azure Container Apps compatibility."""
    pass

@cli.command()
@click.option('--namespace', '-n', help='Kubernetes namespace to analyze. If not specified, analyzes all namespaces.')
@click.option('--exclude-namespaces', help='Comma-separated list of namespaces to exclude from assessment.')
def assess(namespace, exclude_namespaces):
    """Assess Kubernetes applications for ACA compatibility."""
    try:
        # Parse excluded namespaces
        excluded_ns_list = []
        if exclude_namespaces:
            excluded_ns_list = [ns.strip() for ns in exclude_namespaces.split(',') if ns.strip()]
            if excluded_ns_list:
                console.print(f"[yellow]Excluding namespaces: {', '.join(excluded_ns_list)}[/yellow]")

        # Initialize collector and analyzer
        collector = KubernetesCollector()
        analyzer = ACAAnalyzer()

        # Collect deployments
        if namespace:
            console.print(f"[yellow]Collecting deployment information from namespace: {namespace}...[/yellow]")
        else:
            console.print("[yellow]Collecting deployment information from all namespaces...[/yellow]")
            
        deployments = collector.collect_deployments(namespace, excluded_ns_list)

        if not deployments:
            console.print("[red]No deployments found in the specified namespace(s)[/red]")
            return

        # Analyze deployments - progress is shown by the analyzer
        analysis_results = analyzer.analyze_deployments(deployments)

        # Generate and display report
        console.print("\n[green]Analysis complete! Here are the results:[/green]")
        analyzer.generate_report(analysis_results)

    except Exception as e:
        console.print(f"[red]Error during assessment: {str(e)}[/red]")
        raise click.Abort()

if __name__ == '__main__':
    cli()
