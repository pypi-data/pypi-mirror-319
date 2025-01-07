#!/usr/bin/env python3
"""
STRIDE GPT CLI Client

A command-line interface for interacting with the STRIDE GPT API.
Demonstrates the end-to-end threat modeling process.
"""

import sys
import json
import click
import httpx
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress
from typing import List, Dict, Any, Union
from datetime import datetime
from .schemas import (
    Threat, ThreatAnalysisEvaluationRequest, MitigationResponse, RiskAssessment, 
    SecurityControl, MitigationEvaluationRequest, RiskAssessmentEvaluationRequest
)
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Set third-party loggers to WARNING level to reduce noise
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('httpcore').setLevel(logging.WARNING)

console = Console()

class StrideGPTClient:
    """Client for interacting with STRIDE GPT API."""
    
    def __init__(self, base_url: str = "https://api.stridegpt.ai", api_key: str = None):
        self.base_url = base_url
        self.api_key = api_key or os.getenv("STRIDE_GPT_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided either directly or via STRIDE_GPT_API_KEY environment variable")
        
        # Increase timeout to 120 seconds for LLM operations
        self.client = httpx.Client(
            timeout=httpx.Timeout(
                connect=5.0,      # connection timeout
                read=120.0,       # read timeout
                write=5.0,        # write timeout
                pool=5.0         # pool timeout
            ),
            headers={"X-API-Key": self.api_key}
        )
    
    def analyze_threats(self, system_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a system for threat analysis."""
        # Use even longer timeout for initial threat analysis
        with self.client.stream("POST", f"{self.base_url}/api/v1/analyze", json=system_data, timeout=180.0) as response:
            response.raise_for_status()
            content = response.read().decode('utf-8')
            return json.loads(content)
    
    def assess_risk(self, threat: Dict[str, Any], components: List[Dict[str, Any]], 
                  all_threats: List[Dict[str, Any]], 
                  existing_controls: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get risk assessment for a specific threat."""
        request_data = {
            "threat": threat,
            "system_components": components,
            "related_threats": [t for t in all_threats if t["id"] != threat["id"]],
            "existing_controls": existing_controls
        }
        response = self.client.post(f"{self.base_url}/api/v1/assess", json=request_data)
        response.raise_for_status()
        return response.json()
    
    def generate_mitigations(self, threat: Dict[str, Any], risk_assessment: Dict[str, Any] = None, 
                           all_threats: List[Dict[str, Any]] = None,
                           existing_controls: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get mitigation strategies for a threat."""
        request_data = {
            "threat": threat,
            "risk_assessment": risk_assessment,
            "related_threats": [t for t in (all_threats or []) if t["id"] != threat["id"]],
            "existing_controls": existing_controls or []
        }
        
        # Log the request data for debugging
        logger = logging.getLogger(__name__)
        logger.debug(f"Mitigation request data: {json.dumps(request_data, indent=2)}")
        
        response = self.client.post(f"{self.base_url}/api/v1/mitigate", json=request_data)
        response.raise_for_status()
        
        result = response.json()
        logger.debug(f"Mitigation response: {json.dumps(result, indent=2)}")
        return result
    
    def evaluate_threat_identification_prompt(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """[ADMIN ONLY] Evaluate a threat identification prompt template."""
        response = self.client.post(f"{self.base_url}/api/v1/evaluate/identify", json=request)
        response.raise_for_status()
        return response.json()

    def evaluate_mitigation_template(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """[ADMIN ONLY] Evaluate a mitigation prompt template."""
        response = self.client.post(f"{self.base_url}/api/v1/evaluate/mitigation", json=request)
        response.raise_for_status()
        return response.json()

    def evaluate_risk_assessment_prompt(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """[ADMIN ONLY] Evaluate a risk assessment prompt template."""
        response = self.client.post(f"{self.base_url}/api/v1/evaluate/assess", json=request)
        response.raise_for_status()
        return response.json()

def display_threats(threats: List[Dict[str, Any]], summary: str):
    """Display identified threats in a formatted table."""
    table = Table(title="Identified Threats")
    
    # Add columns without wrap parameter
    table.add_column("ID", style="cyan")
    table.add_column("Category", style="magenta")
    table.add_column("Target", style="yellow")
    table.add_column("Description")
    table.add_column("Attack Vectors")
    
    for threat in threats:
        table.add_row(
            threat["id"][:8],  # Truncate ID for display
            threat["category"],
            threat["target_component"],
            threat["description"],
            "\n".join(threat["attack_vectors"])
        )
    
    console.print(table)
    console.print(f"\n[bold]Analysis Summary:[/bold]\n{summary}")

def display_dread_scores(dread_scores: Dict[str, Dict[str, Union[int, str]]]):
    """Display DREAD scoring components in a formatted table."""
    table = Table(title="DREAD Scoring Components")
    table.add_column("Component", style="cyan")
    table.add_column("Score", style="magenta")
    table.add_column("Justification")

    components = [
        ("Damage Potential", "damage_potential"),
        ("Reproducibility", "reproducibility"),
        ("Exploitability", "exploitability"),
        ("Affected Users", "affected_users"),
        ("Discoverability", "discoverability")
    ]

    for display_name, key in components:
        if key in dread_scores:
            table.add_row(
                display_name,
                str(dread_scores[key]["score"]),
                dread_scores[key]["justification"]
            )

    console.print(table)

def display_risk_assessment(assessment: Dict[str, Any], justification: str, has_controls: bool = False):
    """Display risk assessment results using DREAD methodology."""
    if "dread_scores" not in assessment:
        raise ValueError("Risk assessment response is not in DREAD format. The API may need to be updated.")
    
    # Display DREAD scores
    table = Table(title="DREAD Risk Assessment")
    table.add_column("Component", style="cyan")
    if has_controls:
        table.add_column("Inherent", style="red")
        table.add_column("Residual", style="yellow")
    else:
        table.add_column("Score", style="yellow")
    table.add_column("Justification")
    
    # Add DREAD components in order
    dread_components = [
        ("Damage Potential", "damage_potential"),
        ("Reproducibility", "reproducibility"),
        ("Exploitability", "exploitability"),
        ("Affected Users", "affected_users"),
        ("Discoverability", "discoverability")
    ]
    
    # Calculate scores while displaying components
    scores = []
    inherent_scores = []
    residual_scores = []
    
    for display_name, component_key in dread_components:
        component_data = assessment["dread_scores"][component_key]
        if has_controls:
            inherent_score = float(component_data["inherent_score"])
            residual_score = float(component_data["score"])
            inherent_scores.append(inherent_score)
            residual_scores.append(residual_score)
            table.add_row(
                display_name,
                str(inherent_score),
                str(residual_score),
                component_data["justification"]
            )
        else:
            score = float(component_data["score"])
            scores.append(score)
            table.add_row(
                display_name,
                str(score),
                component_data["justification"]
            )
    
    console.print(table)
    
    # Display overall DREAD scores with appropriate color
    if has_controls:
        inherent_score = sum(inherent_scores) / len(inherent_scores)
        residual_score = sum(residual_scores) / len(residual_scores)
        inherent_color = "red" if inherent_score >= 7 else "yellow" if inherent_score >= 4 else "green"
        residual_color = "red" if residual_score >= 7 else "yellow" if residual_score >= 4 else "green"
        console.print(f"\n[bold {inherent_color}]Inherent Risk: {inherent_score:.1f}/10[/bold {inherent_color}] → "
                     f"[bold {residual_color}]Residual Risk: {residual_score:.1f}/10[/bold {residual_color}]")
        
        # Display control impact if available
        if assessment.get("control_impact_summary"):
            console.print("\n[bold]Control Impact:[/bold]")
            console.print(assessment["control_impact_summary"])
            
            if assessment.get("control_risk_reduction"):
                table = Table(title="Control Risk Reduction")
                table.add_column("Control", style="cyan")
                table.add_column("Risk Reduction Effect")
                
                for control, effect in assessment["control_risk_reduction"].items():
                    table.add_row(control, effect)
                
                console.print(table)
    else:
        score = sum(scores) / len(scores)
        score_color = "red" if score >= 7 else "yellow" if score >= 4 else "green"
        console.print(f"\n[bold {score_color}]DREAD Score: {score:.1f}/10[/bold {score_color}]")

def get_risk_level_display(score: float) -> str:
    """Get a formatted risk level string based on the score."""
    if score >= 7:
        return "[red]High[/red]"
    elif score >= 4:
        return "[yellow]Medium[/yellow]"
    return "[green]Low[/green]"

def display_mitigations(result: dict):
    """Display mitigation strategies in a formatted table."""
    table = Table(title="Mitigation Strategies", show_header=True)
    table.add_column("Category", style="cyan", width=20)
    table.add_column("Details", style="green", width=80)

    # Convert lists to strings for display
    table.add_row("Mitigations", "\n".join(f"• {m}" for m in result["mitigations"]))
    table.add_row("Implementation Notes", result["implementation_notes"])
    table.add_row("Priority", result["priority"])
    if "additional_considerations" in result:
        table.add_row("Additional Considerations", "\n".join(f"• {c}" for c in result["additional_considerations"]) if isinstance(result["additional_considerations"], list) else result["additional_considerations"])

    console = Console()
    console.print(table)

def display_improvements(result: Dict[str, Any]):
    """Display system description improvements."""
    # Display original description
    console.print(Panel(result["original_description"], title="Original Description", style="yellow"))
    
    # Display suggested improvements
    table = Table(title="Improvement Suggestions")
    table.add_column("Category", style="cyan")
    table.add_column("Details")
    
    table.add_row(
        "Suggested Improvements",
        "\n".join(f"• {improvement}" for improvement in result["suggested_improvements"])
    )
    table.add_row(
        "Missing Aspects",
        "\n".join(f"• {aspect}" for aspect in result["missing_aspects"])
    )
    
    console.print(table)
    
    # Display enhanced description
    console.print(Panel(result["enhanced_description"], title="Enhanced Description", style="green"))
    
    # Display rationale
    console.print(Panel(result["rationale"], title="Improvement Rationale", style="blue"))

def load_security_controls(controls_file: str) -> List[Dict[str, Any]]:
    """Load security controls from a JSON file."""
    try:
        with open(controls_file) as f:
            controls = json.load(f)
        # Validate the controls format
        required_fields = ["name", "type", "description", "components_covered", 
                         "control_strength", "implementation_status"]
        for control in controls:
            missing_fields = [field for field in required_fields if field not in control]
            if missing_fields:
                raise ValueError(f"Control missing required fields: {', '.join(missing_fields)}")
        return controls
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON in controls file")
    except Exception as e:
        raise ValueError(f"Error loading controls: {str(e)}")

def display_security_controls(controls: List[Dict[str, Any]]):
    """Display security controls in a formatted table."""
    table = Table(title="Security Controls")
    
    table.add_column("Name", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Strength", style="yellow")
    table.add_column("Status")
    table.add_column("Components Covered")
    
    for control in controls:
        table.add_row(
            control["name"],
            control["type"],
            control["control_strength"],
            control["implementation_status"],
            ", ".join(control["components_covered"])
        )
    
    console.print(table)

@click.group()
def cli():
    """STRIDE GPT - Threat Modeling CLI"""
    pass

@cli.command(name='analyze-all')
@click.argument('system_file', type=click.Path(exists=True))
@click.option('--api-url', default="https://api.stridegpt.ai", help="STRIDE GPT API URL")
@click.option('--api-key', envvar='STRIDE_GPT_API_KEY', help="API key for authentication")
@click.option('--output', help="Output file path (default: system_name_analysis.json)")
@click.option('--controls', type=click.Path(exists=True), help="JSON file containing existing security controls")
def analyze_all(system_file: str, api_url: str, api_key: str, output: str, controls: str):
    """Perform complete threat analysis workflow (identification, risk assessment, and mitigation)."""
    try:
        # Load system description
        with open(system_file) as f:
            system_data = json.load(f)
        
        # Load security controls if provided
        existing_controls = None
        if controls:
            existing_controls = load_security_controls(controls)
            console.print("\n=== Existing Security Controls ===")
            display_security_controls(existing_controls)
        
        client = StrideGPTClient(api_url, api_key)
        
        # Initialize results dictionary
        results = {
            "system_name": system_data["system_name"],
            "system_description": system_data["system_description"],
            "components": system_data["components"],
            "existing_controls": existing_controls,
            "threats": [],
            "risk_assessments": {},
            "mitigations": {},
            "analysis_summary": "",
            "assessment_date": datetime.now().isoformat()
        }
        
        with Progress() as progress:
            # Step 1: Identify threats
            task1 = progress.add_task("[cyan]Identifying threats...", total=1)
            result = client.analyze_threats(system_data)
            results["threats"] = result["threats"]
            results["analysis_summary"] = result["analysis_summary"]
            progress.update(task1, completed=1)
            
            console.print("\n=== Identified Threats ===")
            display_threats(results["threats"], results["analysis_summary"])
            
            # Step 2: Assess risks for each threat
            console.print("\n=== Risk Assessments ===")
            task2 = progress.add_task("[yellow]Assessing risks...", total=len(results["threats"]))
            
            for threat in results["threats"]:
                risk_result = client.assess_risk(
                    threat=threat,
                    components=system_data["components"],
                    all_threats=results["threats"],
                    existing_controls=existing_controls
                )
                console.print(f"\nThreat: {threat['description']}")
                display_risk_assessment(risk_result["assessment"], risk_result["justification"], bool(existing_controls))
                
                # Store risk assessment
                results["risk_assessments"][threat["id"]] = {
                    "assessment": risk_result["assessment"],
                    "justification": risk_result["justification"]
                }
                
                # Step 3: Generate mitigations
                mitigation_result = client.generate_mitigations(
                    threat=threat,
                    risk_assessment=risk_result["assessment"],
                    all_threats=results["threats"],
                    existing_controls=existing_controls
                )
                console.print("\n=== Mitigation Strategies ===")
                display_mitigations(mitigation_result)
                
                # Store mitigation strategies
                results["mitigations"][threat["id"]] = mitigation_result
                
                progress.update(task2, advance=1)
                console.print("\n" + "="*80 + "\n")
        
        # Generate output filename if not provided
        if not output:
            system_name = system_data["system_name"].lower().replace(" ", "_")
            output = f"{system_name}_analysis.json"
        
        # Save results to file
        with open(output, 'w') as f:
            json.dump(results, f, indent=2)
        
        console.print(f"\n[green]Complete analysis saved to: {output}")
    
    except httpx.HTTPError as e:
        console.print(f"[red]Error communicating with API: {str(e)}")
        sys.exit(1)
    except json.JSONDecodeError:
        console.print("[red]Error: Invalid JSON in system description or controls file")
        sys.exit(1)
    except ValueError as e:
        console.print(f"[red]Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error: {str(e)}")
        sys.exit(1)

@cli.command()
def template():
    """Generate a template system description file."""
    template_data = {
        "system_name": "Example System",
        "system_description": "Description of your system",
        "components": [
            {
                "name": "Component1",
                "type": "service",
                "description": "Description of the component",
                "data_processed": ["data type 1", "data type 2"],
                "interfaces": ["interface 1", "interface 2"]
            }
        ]
    }
    
    console.print(json.dumps(template_data, indent=2))

@cli.command(name='assess')
@click.argument('threat_file', type=click.Path(exists=True))
@click.option('--api-url', default="https://api.stridegpt.ai", help="STRIDE GPT API URL")
@click.option('--api-key', envvar='STRIDE_GPT_API_KEY', help="API key for authentication")
@click.option('--controls', type=click.Path(exists=True), help="JSON file containing existing security controls")
@click.option('--threat-id', help="Optional: Assess a specific threat by ID")
@click.option('--output', help="Output file path (default: system_name_risk_assessment.json)")
def assess_threats(threat_file: str, api_url: str, api_key: str, controls: str, threat_id: str, output: str):
    """Perform a DREAD risk assessment for a list of identified threats. Optionally specify a threat ID to assess a single threat."""
    try:
        # Load threat data
        with open(threat_file) as f:
            threat_data = json.load(f)
        
        # Load security controls if provided
        existing_controls = None
        if controls:
            existing_controls = load_security_controls(controls)
            console.print("\n=== Existing Security Controls ===")
            display_security_controls(existing_controls)
        
        client = StrideGPTClient(api_url, api_key)

        # Handle both single threat and multiple threats formats
        threats = []
        components = threat_data.get("components", [])
        if "threats" in threat_data:
            # Multiple threats format
            threats = threat_data["threats"]
        elif "threat" in threat_data:
            # Single threat format
            threats = [threat_data["threat"]]
            
        # Filter by threat ID if specified
        if threat_id:
            threats = [t for t in threats if t.get("id", "").startswith(threat_id)]
            if not threats:
                raise ValueError(f"No threat found with ID starting with '{threat_id}'")
        
        # Initialize results dictionary
        results = {
            "threats": threats,
            "components": components,
            "risk_assessments": {},
            "assessment_date": datetime.now().isoformat(),
            "existing_controls": existing_controls
        }
        
        with Progress() as progress:
            task = progress.add_task("[yellow]Assessing risks...", total=len(threats))
            
            for threat in threats:
                console.print(f"\n=== Assessing Threat: {threat['description']} ===")
                
                # Perform risk assessment
                risk_result = client.assess_risk(
                    threat=threat,
                    components=components,
                    all_threats=threats,
                    existing_controls=existing_controls
                )
                
                # Store risk assessment result
                results["risk_assessments"][threat["id"]] = {
                    "assessment": risk_result["assessment"],
                    "justification": risk_result["justification"]
                }
                
                display_risk_assessment(risk_result["assessment"], risk_result["justification"], bool(existing_controls))
                progress.update(task, advance=1)
                
                if len(threats) > 1:
                    console.print("\n" + "="*80 + "\n")
        
        # Generate output filename if not provided
        if not output:
            system_name = threat_data.get("system_name", "threats").lower().replace(" ", "_")
            output = f"{system_name}_risk_assessment.json"
        
        # Save results to file
        with open(output, 'w') as f:
            json.dump(results, f, indent=2)
        
        console.print(f"\n[green]Risk assessment results saved to: {output}")
    
    except httpx.HTTPError as e:
        console.print(f"[red]Error communicating with API: {str(e)}")
        sys.exit(1)
    except json.JSONDecodeError:
        console.print("[red]Error: Invalid JSON in threat file")
        sys.exit(1)
    except ValueError as e:
        console.print(f"[red]Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {str(e)}")
        sys.exit(1)

@cli.command(name='mitigate')
@click.argument('threat_file', type=click.Path(exists=True))
@click.option('--api-url', default="https://api.stridegpt.ai", help="STRIDE GPT API URL")
@click.option('--api-key', envvar='STRIDE_GPT_API_KEY', help="API key for authentication")
@click.option('--controls', type=click.Path(exists=True), help="JSON file containing existing security controls")
@click.option('--threat-id', help="Optional: Generate mitigations for a specific threat by ID")
@click.option('--output', help="Output file path (default: system_name_mitigations.json)")
def generate_mitigations(threat_file: str, api_url: str, api_key: str, controls: str, threat_id: str, output: str):
    """Generate suggested mitigations for a list of identified threats. Optionally specify a threat ID to mitigate a single threat."""
    try:
        # Load threat data
        with open(threat_file) as f:
            threat_data = json.load(f)
        
        # Load security controls if provided
        existing_controls = None
        if controls:
            existing_controls = load_security_controls(controls)
            console.print("\n=== Existing Security Controls ===")
            display_security_controls(existing_controls)
        
        client = StrideGPTClient(api_url, api_key)
        
        # Handle both single threat and multiple threats formats
        threats = []
        if "threats" in threat_data:
            # Multiple threats format
            threats = threat_data["threats"]
        elif "threat" in threat_data:
            # Single threat format
            threats = [threat_data["threat"]]
            
        # Filter by threat ID if specified
        if threat_id:
            threats = [t for t in threats if t.get("id", "").startswith(threat_id)]
            if not threats:
                raise ValueError(f"No threat found with ID starting with '{threat_id}'")
        
        # Initialize results dictionary
        results = {
            "threats": threats,
            "mitigations": {},
            "generation_date": datetime.now().isoformat(),
            "existing_controls": existing_controls
        }
        
        with Progress() as progress:
            task = progress.add_task("[yellow]Generating mitigations...", total=len(threats))
            
            for threat in threats:
                console.print(f"\n=== Generating Mitigations for Threat: {threat['description']} ===")
                
                # Generate mitigations
                mitigation_result = client.generate_mitigations(
                    threat=threat,
                    risk_assessment=threat_data.get("risk_assessments", {}).get(threat["id"]),
                    all_threats=threats,
                    existing_controls=existing_controls
                )
                
                # Store mitigation result
                results["mitigations"][threat["id"]] = mitigation_result
                
                display_mitigations(mitigation_result)
                progress.update(task, advance=1)
                
                if len(threats) > 1:
                    console.print("\n" + "="*80 + "\n")
        
        # Generate output filename if not provided
        if not output:
            system_name = threat_data.get("system_name", "threats").lower().replace(" ", "_")
            output = f"{system_name}_mitigations.json"
        
        # Save results to file
        with open(output, 'w') as f:
            json.dump(results, f, indent=2)
        
        console.print(f"\n[green]Mitigation strategies saved to: {output}")
    
    except httpx.HTTPError as e:
        console.print(f"[red]Error communicating with API: {str(e)}")
        sys.exit(1)
    except json.JSONDecodeError:
        console.print("[red]Error: Invalid JSON in threat file")
        sys.exit(1)
    except ValueError as e:
        console.print(f"[red]Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {str(e)}")
        sys.exit(1)

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--format', type=click.Choice(['json', 'yaml', 'csv']), default='json', help="Output format")
def export(input_file: str, output_file: str, format: str):
    """Export threat analysis results to different formats."""
    try:
        # Load the threat analysis data
        with open(input_file) as f:
            data = json.load(f)

        if format == 'json':
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
        elif format == 'yaml':
            import yaml
            with open(output_file, 'w') as f:
                yaml.dump(data, f)
        elif format == 'csv':
            import csv
            with open(output_file, 'w', newline='') as f:
                writer = csv.writer(f)
                # Write headers
                writer.writerow(['ID', 'Category', 'Target', 'Description', 'Attack Vectors', 
                               'Risk Score', 'Impact', 'Likelihood'])
                # Write threat data
                for threat in data.get("threats", []):
                    risk = data.get("risk_assessments", {}).get(threat["id"], {})
                    writer.writerow([
                        threat["id"],
                        threat["category"],
                        threat["target_component"],
                        threat["description"],
                        "; ".join(threat["attack_vectors"]),
                        risk.get("risk_score", "N/A"),
                        risk.get("impact", "N/A"),
                        risk.get("likelihood", "N/A")
                    ])

        console.print(f"[green]Successfully exported to {output_file}")

    except Exception as e:
        console.print(f"[red]Error: {str(e)}")
        sys.exit(1)

@cli.command()
@click.argument('system_file', type=click.Path(exists=True))
@click.option('--api-url', default="https://api.stridegpt.ai", help="STRIDE GPT API URL")
@click.option('--api-key', envvar='STRIDE_GPT_API_KEY', help="API key for authentication")
@click.option('--output', help="Output file path (default: system_name_threats_identified.json)")
def identify(system_file: str, api_url: str, api_key: str, output: str):
    """Identify threats in a system (without risk assessment or mitigation)."""
    try:
        # Load system description
        with open(system_file) as f:
            system_data = json.load(f)
        
        client = StrideGPTClient(api_url, api_key)
        
        # Initialize results dictionary
        results = {
            "system_name": system_data["system_name"],
            "system_description": system_data["system_description"],
            "components": system_data["components"],
            "threats": [],
            "analysis_summary": "",
            "analysis_date": datetime.now().isoformat()
        }
        
        with Progress() as progress:
            # Identify threats
            task = progress.add_task("[cyan]Identifying threats...", total=1)
            result = client.analyze_threats(system_data)
            results["threats"] = result["threats"]
            results["analysis_summary"] = result["analysis_summary"]
            progress.update(task, completed=1)
            
            console.print("\n=== Threat Analysis Results ===")
            display_threats(results["threats"], results["analysis_summary"])
        
        # Generate output filename if not provided
        if not output:
            system_name = system_data["system_name"].lower().replace(" ", "_")
            output = f"{system_name}_threats_identified.json"
        
        # Save results to file
        with open(output, 'w') as f:
            json.dump(results, f, indent=2)
        
        console.print(f"\n[green]Identified threats saved to: {output}")
        console.print("\n[yellow]To perform complete threat analysis with risk assessment and mitigations, run:")
        console.print(f"stride-gpt analyze-all {system_file}")
    
    except httpx.HTTPError as e:
        console.print(f"[red]Error communicating with API: {str(e)}")
        sys.exit(1)
    except json.JSONDecodeError:
        console.print("[red]Error: Invalid JSON in system description file")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {str(e)}")
        sys.exit(1)

@cli.command()
@click.argument('system_file', type=click.Path(exists=True))
@click.option('--api-url', default="https://api.stridegpt.ai", help="STRIDE GPT API URL")
@click.option('--api-key', envvar='STRIDE_GPT_API_KEY', help="API key for authentication")
@click.option('--output', help="Output file path (default: system_name_improved.json)")
def improve(system_file: str, api_url: str, api_key: str, output: str):
    """Get suggestions to improve system description for better threat modeling."""
    try:
        # Load system description
        with open(system_file) as f:
            system_data = json.load(f)
        
        client = StrideGPTClient(api_url, api_key)
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Analyzing system description...", total=1)
            
            # Call the improve endpoint
            response = client.client.post(
                f"{client.base_url}/api/v1/improve",
                json=system_data
            )
            response.raise_for_status()
            result = response.json()
            
            progress.update(task, completed=1)
            
            # Display improvements
            console.print("\n=== System Description Improvements ===")
            display_improvements(result)
            
            # Generate output filename if not provided
            if not output:
                system_name = system_data["system_name"].lower().replace(" ", "_")
                output = f"{system_name}_improved.json"
            
            # Save results to file
            with open(output, 'w') as f:
                json.dump(result, f, indent=2)
            
            console.print(f"\n[green]Improvement suggestions saved to: {output}")
    
    except httpx.HTTPError as e:
        console.print(f"[red]Error communicating with API: {str(e)}")
        sys.exit(1)
    except json.JSONDecodeError:
        console.print("[red]Error: Invalid JSON in system description file")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {str(e)}")
        sys.exit(1)

@cli.command(name='controls-template')
def controls_template():
    """Generate a template security controls file."""
    template_data = [
        {
            "name": "Access Control System",
            "type": "preventive",
            "description": "Role-based access control system with MFA",
            "components_covered": ["api-gateway", "user-service"],
            "control_strength": "Strong",
            "implementation_status": "Implemented",
            "last_assessment_date": "2024-01-01",
            "standards_compliance": ["ISO27001", "NIST SP 800-53"]
        },
        {
            "name": "Audit Logging",
            "type": "detective",
            "description": "Comprehensive system-wide audit logging",
            "components_covered": ["all"],
            "control_strength": "Medium",
            "implementation_status": "Partially Implemented",
            "last_assessment_date": "2023-12-15",
            "standards_compliance": ["SOX", "PCI-DSS"]
        }
    ]
    
    # Add helpful comments as a header
    template_with_comments = {
        "comments": {
            "description": "Template for defining existing security controls",
            "fields": {
                "name": "Unique name of the control",
                "type": "One of: preventive, detective, corrective, deterrent",
                "description": "Detailed description of what the control does",
                "components_covered": "List of component names this control applies to (use 'all' for system-wide)",
                "control_strength": "One of: Strong, Medium, Weak",
                "implementation_status": "One of: Implemented, Partially Implemented, Planned, Not Implemented",
                "last_assessment_date": "When the control was last reviewed (YYYY-MM-DD)",
                "standards_compliance": "Optional: List of security standards this control helps comply with"
            }
        },
        "controls": template_data
    }
    
    console.print(json.dumps(template_with_comments, indent=2))
    console.print("\n[yellow]Note: Remove the 'comments' section before using this file with other commands.")
    console.print("[yellow]Tip: Save this template using: stride-gpt controls-template > controls.json")

@cli.group(name='evaluate')
def evaluate():
    """[ADMIN ONLY] Evaluate prompt templates to identify possible improvements."""
    pass

@evaluate.command(name='identify')
@click.argument('prompt_file', type=click.Path(exists=True))
@click.argument('threats_file', type=click.Path(exists=True))
@click.option('--api-url', default="https://api.stridegpt.ai", help="STRIDE GPT API URL")
@click.option('--api-key', envvar='STRIDE_GPT_API_KEY', help="API key for authentication")
@click.option('--output', help="Output file path (default: identify_prompt_evaluation.json)")
def evaluate_identification_prompt(prompt_file: str, threats_file: str, api_url: str, api_key: str, output: str):
    """[ADMIN ONLY]Evaluate a threat identification prompt template using existing analysis results."""
    try:
        # Load prompt template
        with open(prompt_file, 'r') as f:
            prompt_template = f.read()
        
        # Load threats data
        with open(threats_file) as f:
            threat_data = json.load(f)
        
        # Handle both single threat and multiple threats formats
        threats = []
        if "threats" in threat_data:
            threats = threat_data["threats"]
        elif "threat" in threat_data:
            threats = [threat_data["threat"]]
        
        if not threats:
            raise ValueError("No threats found in the threats file")
        
        client = StrideGPTClient(api_url, api_key)
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Evaluating threat identification prompt...", total=1)
            
            # Convert threats to Threat objects
            threat_objects = [
                Threat(
                    id=t.get("id", f"THREAT-{i+1}"),
                    category=t["category"],
                    description=t["description"],
                    target_component=t["target_component"],
                    attack_vectors=t["attack_vectors"]
                )
                for i, t in enumerate(threats)
            ]
            
            # Create evaluation request
            request = ThreatAnalysisEvaluationRequest(
                original_prompt=prompt_template,
                threats_identified=threat_objects
            )
            
            # Call evaluation endpoint
            result = client.evaluate_threat_identification_prompt(request.model_dump())
            
            progress.update(task, completed=1)
            
            # Display evaluation results
            console.print("\n=== Threat Identification Prompt Evaluation ===")
            console.print(f"\nQuality Score: {'🟢' if result['evaluation_score'] >= 7 else '🟡' if result['evaluation_score'] >= 5 else '🔴'} {result['evaluation_score']:.1f}/10")
            
            console.print("\n💪 Strengths:")
            for strength in result["strengths"]:
                console.print(f"✓ {strength}")
            
            console.print("\n🎯 Areas for Improvement:")
            for weakness in result["weaknesses"]:
                console.print(f"• {weakness}")
            
            console.print("\n💡 Suggested Improvements:")
            for suggestion in result["suggested_prompt_improvements"]:
                console.print(f"→ {suggestion}")
            
            console.print("\n📋 Improved Prompt Template:")
            console.print("="*80)
            console.print(result["improved_prompt"])
            console.print("="*80)
            
            # Generate output filename if not provided
            if not output:
                output = "identify_prompt_evaluation.json"
            
            # Save results to file
            with open(output, 'w') as f:
                json.dump(result, f, indent=2)
            
            console.print(f"\n[green]Evaluation results saved to: {output}")
    
    except httpx.HTTPError as e:
        console.print(f"[red]Error communicating with API: {str(e)}")
        sys.exit(1)
    except json.JSONDecodeError:
        console.print("[red]Error: Invalid JSON in threats file")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error: {str(e)}")
        sys.exit(1)

@evaluate.command(name='mitigate')
@click.argument('prompt_file', type=click.Path(exists=True))
@click.argument('mitigations_file', type=click.Path(exists=True))
@click.option('--api-url', default="https://api.stridegpt.ai", help="STRIDE GPT API URL")
@click.option('--api-key', envvar='STRIDE_GPT_API_KEY', help="API key for authentication")
@click.option('--output', help="Output file path (default: mitigation_prompt_evaluation.json)")
def evaluate_mitigation_prompt(prompt_file: str, mitigations_file: str, api_url: str, api_key: str, output: str):
    """[ADMIN ONLY] Evaluate a mitigation prompt template using existing mitigation results."""
    try:
        # Set up logging
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        
        # Load prompt template
        with open(prompt_file, 'r') as f:
            prompt_template = f.read()
        logger.debug(f"Loaded prompt template:\n{prompt_template}")
        
        # Load mitigations data
        with open(mitigations_file) as f:
            mitigation_data = json.load(f)
        logger.debug(f"Loaded mitigation data structure: {list(mitigation_data.keys())}")
        
        if not mitigation_data.get("mitigations"):
            raise ValueError("No mitigations found in the mitigations file")
        
        client = StrideGPTClient(api_url, api_key)
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Evaluating mitigation prompt...", total=1)
            
            # Convert mitigations to MitigationResponse objects
            mitigation_responses = []
            for threat_id, mitigation in mitigation_data["mitigations"].items():
                logger.debug(f"Processing mitigation for threat {threat_id}")
                try:
                    # Create MitigationResponse object with validation
                    mitigation_response = MitigationResponse(
                        threat_id=threat_id,
                        target_component=mitigation.get("target_component", ""),
                        mitigations=mitigation.get("mitigations", []),
                        implementation_notes=mitigation.get("implementation_notes", ""),
                        additional_considerations=mitigation.get("additional_considerations", ""),
                        priority=mitigation.get("priority", "Medium"),
                        existing_control_gaps=mitigation.get("existing_control_gaps", []),
                        control_improvements=mitigation.get("control_improvements", [])
                    )
                    mitigation_responses.append(mitigation_response)
                except Exception as e:
                    logger.error(f"Error processing mitigation for threat {threat_id}: {str(e)}")
                    raise ValueError(f"Invalid mitigation data for threat {threat_id}: {str(e)}")
            
            logger.debug(f"Processed {len(mitigation_responses)} mitigation responses")
            
            # Find the corresponding threat in the threats list
            threats_map = {t["id"]: t for t in mitigation_data.get("threats", [])}
            
            # Get the first mitigation's threat
            first_mitigation = next(iter(mitigation_data["mitigations"].items()))
            threat_id = first_mitigation[0]
            threat_data = threats_map.get(threat_id)
            
            if not threat_data:
                logger.warning(f"No threat data found for ID {threat_id}")
                threat_data = {
                    "id": threat_id,
                    "category": "Unknown",
                    "description": "Unknown",
                    "target_component": first_mitigation[1].get("target_component", "Unknown"),
                    "attack_vectors": []
                }
            
            threat = Threat(
                id=threat_data["id"],
                category=threat_data["category"],
                description=threat_data["description"],
                target_component=threat_data["target_component"],
                attack_vectors=threat_data["attack_vectors"]
            )
            
            logger.debug(f"Using threat for evaluation: {threat.model_dump()}")
            
            # Create evaluation request using Pydantic model
            request = MitigationEvaluationRequest(
                original_prompt=prompt_template,
                mitigations_generated=mitigation_responses,
                threat=threat
            )
            
            # Log the request for debugging
            logger.debug(f"Sending evaluation request to {api_url}/api/v1/evaluate/mitigation")
            
            # Call evaluation endpoint
            result = client.evaluate_mitigation_template(request.model_dump())
            
            progress.update(task, completed=1)
            
            # Display evaluation results
            console.print("\n=== Mitigation Prompt Evaluation ===")
            console.print(f"\nQuality Score: {'🟢' if result['evaluation_score'] >= 7 else '🟡' if result['evaluation_score'] >= 5 else '🔴'} {result['evaluation_score']:.1f}/10")
            
            console.print("\n💪 Strengths:")
            for strength in result["strengths"]:
                console.print(f"✓ {strength}")
            
            console.print("\n🎯 Areas for Improvement:")
            for weakness in result["weaknesses"]:
                console.print(f"• {weakness}")
            
            console.print("\n💡 Suggested Improvements:")
            for suggestion in result["suggested_improvements"]:
                console.print(f"→ {suggestion}")
            
            console.print("\n📋 Improved Prompt Template:")
            console.print("="*80)
            console.print(result["improved_prompt"])
            console.print("="*80)
            
            console.print("\n🤔 Evaluation Reasoning:")
            console.print(result["reasoning"])
            
            # Generate output filename if not provided
            if not output:
                output = "mitigation_prompt_evaluation.json"
            
            # Save results to file
            with open(output, 'w') as f:
                json.dump(result, f, indent=2)
            
            console.print(f"\n[green]Evaluation results saved to: {output}")
    
    except httpx.HTTPError as e:
        logger.error(f"HTTP Error: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Response content: {e.response.text}")
            logger.error(f"Response status code: {e.response.status_code}")
            logger.error(f"Response headers: {e.response.headers}")
        console.print(f"[red]Error communicating with API: {str(e)}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error("JSON decode error", exc_info=True)
        logger.error(f"Error location: line {e.lineno}, column {e.colno}")
        console.print("[red]Error: Invalid JSON in mitigations file")
        sys.exit(1)
    except Exception as e:
        logger.error("Unexpected error", exc_info=True)
        console.print(f"[red]Error: {str(e)}")
        sys.exit(1)

@evaluate.command(name='assess')
@click.argument('prompt_file', type=click.Path(exists=True))
@click.argument('assessments_file', type=click.Path(exists=True))
@click.option('--api-url', default="https://api.stridegpt.ai", help="STRIDE GPT API URL")
@click.option('--api-key', envvar='STRIDE_GPT_API_KEY', help="API key for authentication")
@click.option('--controls', type=click.Path(exists=True), help="Optional JSON file containing security controls")
@click.option('--output', help="Output file path (default: risk_assessment_prompt_evaluation.json)")
def evaluate_risk_assessment_prompt(prompt_file: str, assessments_file: str, api_url: str, api_key: str, controls: str, output: str):
    """[ADMIN ONLY] Evaluate a risk assessment prompt template using existing assessment results."""
    try:
        # Load prompt template
        with open(prompt_file) as f:
            prompt_template = f.read().strip()
        
        # Load risk assessments
        with open(assessments_file) as f:
            assessment_data = json.load(f)
        
        # Initialize client
        client = StrideGPTClient(api_url, api_key)
        
        # Set up logging for debugging
        logger = logging.getLogger(__name__)
        logger.debug(f"Loaded assessment data: {json.dumps(assessment_data, indent=2)}")
        
        # Load security controls if provided
        context_controls = None
        if controls:
            controls_data = load_security_controls(controls)
            console.print("\n=== Existing Security Controls ===")
            display_security_controls(controls_data)
            context_controls = [
                SecurityControl(
                    name=c["name"],
                    type=c["type"],
                    description=c["description"],
                    effectiveness=c["effectiveness"],
                    status=c["status"],
                    components_covered=c["components_covered"],
                    control_strength=c["control_strength"],
                    implementation_status=c["implementation_status"],
                    last_assessment_date=c.get("last_assessment_date"),
                    compliance_requirements=c.get("compliance_requirements", [])
                )
                for c in controls_data
            ]
        
        with Progress() as progress:
            task = progress.add_task("[cyan]Evaluating risk assessment prompt...", total=1)
            
            # Convert risk assessments to RiskAssessment objects
            risk_assessments = []
            for assessment in assessment_data.get("risk_assessments", {}).values():
                logger.debug(f"Processing risk assessment: {json.dumps(assessment, indent=2)}")
                try:
                    # Create RiskAssessment object with validation
                    risk_assessment = RiskAssessment(
                        threat_id=assessment["assessment"]["threat_id"],
                        dread_scores=assessment["assessment"]["dread_scores"],
                        overall_risk_score=assessment["assessment"]["overall_risk_score"],
                        risk_factors=assessment["assessment"]["risk_factors"],
                        applicable_controls=assessment["assessment"].get("applicable_controls", []),
                        control_effectiveness=assessment["assessment"].get("control_effectiveness", {})
                    )
                    risk_assessments.append(risk_assessment)
                except Exception as e:
                    logger.error(f"Error processing risk assessment: {str(e)}")
                    raise ValueError(f"Invalid risk assessment data: {str(e)}")
            
            logger.debug(f"Processed {len(risk_assessments)} risk assessments")
            
            # Create evaluation request
            request = RiskAssessmentEvaluationRequest(
                original_prompt=prompt_template,
                risk_assessments=risk_assessments,
                existing_controls=context_controls
            )
            
            # Call evaluation endpoint
            result = client.evaluate_risk_assessment_prompt(request.model_dump())
            
            progress.update(task, completed=1)
            
            # Display evaluation results
            console.print("\n=== Risk Assessment Prompt Evaluation ===")
            console.print(f"\nQuality Score: {'🟢' if result['evaluation_score'] >= 7 else '🟡' if result['evaluation_score'] >= 5 else '🔴'} {result['evaluation_score']:.1f}/10")
            
            console.print("\n💪 Strengths:")
            for strength in result["strengths"]:
                console.print(f"✓ {strength}")
            
            console.print("\n🎯 Areas for Improvement:")
            for weakness in result["weaknesses"]:
                console.print(f"• {weakness}")
            
            console.print("\n💡 Prompt Improvement Suggestions:")
            for suggestion in result["suggested_improvements"]:
                console.print(f"→ {suggestion}")
            
            console.print("\n🎯 DREAD Scoring Quality Analysis:")
            for component, observations in result["dread_scoring_quality"].items():
                console.print(f"\n{component.replace('_', ' ').title()}:")
                for observation in observations:
                    console.print(f"• {observation}")
            
            console.print("\n⚖️ Risk Level Accuracy Assessment:")
            console.print(result["risk_level_accuracy"])
            
            console.print("\n📝 Improved Prompt:")
            console.print("----------------")
            console.print(result["improved_prompt"])
            console.print("----------------")
            
            # Generate output filename if not provided
            if not output:
                output = "risk_assessment_prompt_evaluation.json"
            
            # Save results to file
            with open(output, 'w') as f:
                json.dump(result, f, indent=2)
            
            console.print(f"\n[green]Evaluation results saved to: {output}")
    
    except httpx.HTTPError as e:
        logger.error(f"HTTP Error: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Response content: {e.response.text}")
            logger.error(f"Response status code: {e.response.status_code}")
            logger.error(f"Response headers: {e.response.headers}")
        console.print(f"[red]Error communicating with API: {str(e)}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error("JSON decode error", exc_info=True)
        logger.error(f"Error location: line {e.lineno}, column {e.colno}")
        console.print("[red]Error: Invalid JSON in assessments file")
        sys.exit(1)
    except Exception as e:
        logger.error("Unexpected error", exc_info=True)
        console.print(f"[red]Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    cli() 