# GitHub Copilot Instructions for ACA Assessor Project

## Project Goal
The primary goal is to develop an application that assesses existing applications on a Kubernetes cluster for their suitability and migration path to Azure Container Apps (ACA).

## Your Role as GitHub Copilot
Your main task is to assist in building this ACA assessment tool. You should help with:
1.  **Developing scripts** to automatically collect relevant configuration data from Kubernetes clusters.
2.  **Creating analysis logic** to evaluate the collected data for ACA compatibility.
3.  **Generating reports** in Markdown format that include migration recommendations, potential challenges, and ACA-specific configurations.
4.  **Estimating resource requirements** and potential costs in ACA, utilizing the Azure Retail Prices API (see [Azure Retail Prices API](https://learn.microsoft.com/en-us/rest/api/cost-management/retail-prices/azure-retail-prices) for reference).

## Initial Development Focus
We will start by focusing on the following areas:
1.  **Kubernetes Data Collection**: Scripts and methods to gather information from Kubernetes clusters. This includes:
    *   Accessing Kubernetes cluster manifests (YAML files).
    *   Utilizing `kubectl` commands for inspecting running applications and outputting relevant resource configurations in JSON format.
    *   Identifying the Kubernetes distribution (e.g., AKS, EKS, GKE).
2.  **ACA Compatibility Analysis (Initial Tooling)**: Building the foundational components of the analysis tool. This involves:
    *   Parsing the collected JSON data from Kubernetes.
    *   Comparing the parsed data against the supported features and configurations of Azure Container Apps (referencing the fetched schema).
    *   Evaluating application types (web apps, APIs, background services).
    *   Considering programming languages/frameworks.
    *   Differentiating between stateful and stateless applications.

## Key Information Areas for Assessment
When developing the tool, ensure it can process and analyze the following aspects of the Kubernetes applications:

### 1. Kubernetes Cluster Information
*   Cluster manifests (YAML files).
*   Output from `kubectl` inspection commands.
*   Kubernetes distribution (AKS, EKS, GKE, etc.).

### 2. Application Details
*   Number and types of applications (web apps, APIs, background services).
*   Programming languages and frameworks used.
*   Statefulness (stateful or stateless).

### 3. Container Information
*   Dockerfile content.
*   Container image registries in use.
*   Usage of custom base images.
*   Container probes (liveness, readiness, startup).

### 4. Resource Requirements
*   Current CPU and memory requests/limits.
*   Storage requirements, Persistent Volume Claims (PVCs), and volume mounts.
*   Network configurations (ports, protocols, Ingress, Services), including any Ingress annotations that modify behavior (note: custom Ingress annotations may not be supported in ACA).

### 5. Dependencies
*   Inter-service dependencies within the cluster.
*   External service dependencies (databases, message queues, APIs, etc.).
*   Configuration management (ConfigMaps, environment variables).
*   Secrets management solutions.

### 6. Scaling and Availability
*   Horizontal Pod Autoscaler (HPA) configurations.
*   Availability requirements (replicas, anti-affinity, etc.).
*   Observed traffic patterns and load characteristics.

### 7. Monitoring and Logging
*   Current monitoring solutions in place.
*   Logging architecture and aggregation.
*   Specific observability requirements.

## Important Considerations for the Tool
Keep these points in mind during development:
*   **Namespace Usage**: How are namespaces utilized? Can we assume one namespace per application, or is it more complex?
*   **Deployment Methods**: How are applications currently deployed (e.g., Helm, Kustomize, raw YAML files)?
*   **Workload Types**: Are applications primarily deployed as Deployments, StatefulSets, DaemonSets, etc.?

## Development Tooling
*   This project uses Poetry for Python dependency management. Ensure that the project structure and any dependency modifications are compatible with Poetry.

## ACA Best Practices and Limitations
As we build the tool, incorporate Azure Container Apps best practices and limitations to ensure the assessment provides realistic and actionable recommendations. You should help identify and apply these as relevant.

Refer to the official Azure Container Apps schema for supported configurations and fetch the content from this URL to ensure up-to-date information: https://learn.microsoft.com/en-us/azure/templates/microsoft.app/containerapps?pivots=deployment-language-bicep

### Cost Estimation
*   Utilize the Azure Retail Prices API to provide cost estimates for the recommended ACA configurations.
*   The tool should allow the user to specify an Azure region for pricing. If no region is provided, attempt to infer a suitable region.
    *   To infer the region from the machine's timezone:
        *   Attempt to retrieve the system's IANA timezone name (e.g., using `systemsetup -gettimezone` on macOS, or `timedatectl status | grep 'Time zone'` on Linux).
        *   Implement a heuristic mapping from common IANA timezone names/prefixes (e.g., 'America/', 'Europe/', 'Asia/', 'Australia/') to a suitable Azure region from the [Azure regions list](https://learn.microsoft.com/en-us/azure/reliability/regions-list). This list should be periodically updated within the tool. Examples:
            *   'America/New_York' -> 'East US'
            *   'America/Chicago' -> 'Central US'
            *   'America/Denver' -> 'West Central US'
            *   'America/Los_Angeles' -> 'West US'
            *   'Europe/London' -> 'UK South'
            *   'Europe/Paris' -> 'France Central'
            *   'Europe/Berlin' -> 'Germany West Central'
            *   'Asia/Tokyo' -> 'Japan East'
            *   'Asia/Singapore' -> 'Southeast Asia'
            *   'Australia/Sydney' -> 'Australia East'
        *   This mapping should be maintained within the tool. If a clear mapping cannot be determined, fall back to a default common region (e.g., 'East US').
*   Base the cost estimation on the gathered resource requirements (CPU, memory, storage, etc.) and map them to appropriate ACA SKUs and pricing tiers.

## Tool Development and Quality
*   **Error Handling and Logging**: Implement robust error handling and logging within the ACA Assessor tool to aid in debugging and provide clear feedback to the user.
*   **Testing**: Develop unit and integration tests for the ACA Assessor tool to ensure its accuracy and reliability.

This structured approach will help us build an effective assessment tool.
