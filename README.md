# ACA Assessor

A tool to assess Kubernetes applications for Azure Container Apps compatibility.

## Features

- Analyzes Kubernetes deployments for ACA compatibility
- Checks resource limits and requirements
- Validates volume configurations
- Analyzes networking settings
- Provides compatibility scores and recommendations
- Generates detailed reports

## Installation

1. Clone the repository
2. Install the package:

```bash
pip install -e .
```

## Prerequisites

- Python 3.8 or higher
- Access to a Kubernetes cluster (configured kubectl)
- Azure CLI (optional, for Azure-related features)

## Usage

To assess all applications in your Kubernetes cluster:

```bash
aca-assess assess
```

To assess applications in a specific namespace:

```bash
aca-assess assess --namespace my-namespace
```

## Assessment Criteria

The tool checks for:

- Resource limits (CPU and memory) compatibility
- Volume types and configurations
- Network protocols and ports
- Scaling configurations
- Environment variables and secrets
- Container configurations

## Report Format

The assessment generates a report showing:

- Compatibility score for each application
- Identified issues
- Specific recommendations
- Resource usage analysis

## Example

Command to assess a specific namespace:

```bash
aca-assess assess --namespace my-wordpress
```

Example output:

![Example Assessment Report](docs/example-report.png)


## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

This project is licensed under the MIT License.
