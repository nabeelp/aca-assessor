"""
Command-line interface for ACA Assessor.
"""
import click
import os
from rich.console import Console
from .collector import KubernetesCollector
from .analyzer import ACAAnalyzer
from .config import load_config, get_excluded_namespaces, create_default_config

console = Console()

@click.group()
def cli():
    """ACA Assessor - Analyze Kubernetes applications for Azure Container Apps compatibility."""
    pass

@cli.command()
@click.option('--namespace', '-n', help='Kubernetes namespace to analyze. If not specified, analyzes all namespaces.')
@click.option('--config', '-c', help='Path to configuration file.')
@click.option('--init-config', is_flag=True, help='Initialize a default configuration file in the current directory.')
def assess(namespace, config, init_config):
    """Assess Kubernetes applications for ACA compatibility."""
    try:
        # Handle config file initialization if requested
        if init_config:
            config_path = os.path.join(os.getcwd(), "aca-assessor.yaml")
            if create_default_config(config_path):
                console.print(f"[green]Created default configuration file at: {config_path}[/green]")
                console.print("[yellow]Edit this file to configure namespace exclusions and other settings.[/yellow]")
                return
            else:
                console.print("[red]Failed to create configuration file.[/red]")
                return

        # Load configuration
        config_data = load_config(config)
        
        # Get excluded namespaces from config
        excluded_ns_list = get_excluded_namespaces(config_data)
        if excluded_ns_list:
            console.print(f"[yellow]Excluding namespaces from config: {', '.join(excluded_ns_list)}[/yellow]")

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
