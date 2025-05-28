"""
Configuration module for ACA Assessor.
Handles loading and parsing configuration files.
"""
import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from rich.console import Console

console = Console()

# Default config file locations
DEFAULT_CONFIG_LOCATIONS = [
    os.path.join(os.path.expanduser("~"), ".aca-assessor.yaml"),  # User home directory
    os.path.join(os.getcwd(), ".aca-assessor.yaml"),              # Current working directory
    os.path.join(os.getcwd(), "aca-assessor.yaml")                # Current working directory (alternative)
]

# Default configuration
DEFAULT_CONFIG = {
    "assessment": {
        "excluded_namespaces": []  # Default: no exclusions
    }
}


def get_config_path() -> Optional[str]:
    """Find the first available configuration file in default locations."""
    for path in DEFAULT_CONFIG_LOCATIONS:
        if os.path.exists(path):
            return path
    return None


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from file. If no file path provided,
    searches for config in default locations.
    """
    # Try to find config if no path provided
    if not config_path:
        config_path = get_config_path()
    
    # If still no config, return defaults
    if not config_path or not os.path.exists(config_path):
        return DEFAULT_CONFIG
        
    # Load config from file
    try:
        with open(config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
            if not config:
                return DEFAULT_CONFIG
                
            # Ensure config has required structure
            if 'assessment' not in config:
                config['assessment'] = {}
            if 'excluded_namespaces' not in config['assessment']:
                config['assessment']['excluded_namespaces'] = []
                
            return config
    except Exception as e:
        console.print(f"[yellow]Warning: Failed to load config from {config_path}: {str(e)}[/yellow]")
        console.print("[yellow]Using default configuration...[/yellow]")
        return DEFAULT_CONFIG


def get_excluded_namespaces(config: Dict[str, Any]) -> List[str]:
    """Extract and normalize excluded namespaces from configuration."""
    excluded = config.get('assessment', {}).get('excluded_namespaces', [])
    
    # Handle case when excluded_namespaces is provided as a string
    if isinstance(excluded, str):
        excluded = [ns.strip() for ns in excluded.split(',') if ns.strip()]
        
    # Ensure it's a list and items are strings
    if not isinstance(excluded, list):
        excluded = []
        
    # Remove duplicates while preserving order
    unique_excluded = []
    for ns in excluded:
        if ns not in unique_excluded and isinstance(ns, str):
            unique_excluded.append(ns)
            
    return unique_excluded


def create_default_config(path: str) -> bool:
    """Create a default configuration file at the specified path."""
    try:
        # Create parent directories if they don't exist
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        
        # Create the default config with comments
        default_config_with_comments = """# ACA Assessor Configuration File

assessment:
  # List of namespaces to exclude from assessment
  # These namespaces will be skipped when collecting deployments
  excluded_namespaces:
    - kube-system
    - kube-public
    - kube-node-lease
"""
        
        with open(path, 'w') as config_file:
            config_file.write(default_config_with_comments)
            
        return True
    except Exception as e:
        console.print(f"[red]Error creating config file: {str(e)}[/red]")
        return False