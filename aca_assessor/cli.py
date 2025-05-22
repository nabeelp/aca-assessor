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
def assess(namespace):
    """Assess Kubernetes applications for ACA compatibility."""
    try:
        # Initialize collector and analyzer
        collector = KubernetesCollector()
        analyzer = ACAAnalyzer()

        # Collect deployments
        console.print("[yellow]Collecting deployment information...[/yellow]")
        deployments = collector.collect_deployments(namespace)

        if not deployments:
            console.print("[red]No deployments found in the specified namespace(s)[/red]")
            return

        # Analyze deployments
        console.print("[yellow]Analyzing compatibility with Azure Container Apps...[/yellow]")
        analysis_results = analyzer.analyze_deployments(deployments)

        # Generate and display report
        console.print("\n[green]Analysis complete! Here are the results:[/green]")
        analyzer.generate_report(analysis_results)

    except Exception as e:
        console.print(f"[red]Error during assessment: {str(e)}[/red]")
        raise click.Abort()

if __name__ == '__main__':
    cli()
