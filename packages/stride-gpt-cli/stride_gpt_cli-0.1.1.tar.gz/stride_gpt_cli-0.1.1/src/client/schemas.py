"""Data models for the STRIDE GPT CLI."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class Threat(BaseModel):
    """Threat model."""
    id: str
    category: str
    target_component: str
    description: str
    attack_vectors: List[str]


class ThreatAnalysisEvaluationRequest(BaseModel):
    """Request model for threat analysis evaluation."""
    system_description: Dict[str, Any]
    expected_threats: List[Dict[str, Any]]


class MitigationResponse(BaseModel):
    """Response model for mitigation strategies."""
    mitigations: List[Dict[str, Any]]
    implementation_notes: Optional[str] = None
    priority: Optional[str] = None


class RiskAssessment(BaseModel):
    """Risk assessment model."""
    dread_scores: Dict[str, Dict[str, Any]]
    justification: str
    control_impact_summary: Optional[str] = None
    control_risk_reduction: Optional[Dict[str, str]] = None


class SecurityControl(BaseModel):
    """Security control model."""
    name: str
    type: str
    description: str
    components_covered: List[str]
    control_strength: str
    implementation_status: str
    last_assessment_date: str
    standards_compliance: Optional[List[str]] = None


class MitigationEvaluationRequest(BaseModel):
    """Request model for mitigation evaluation."""
    threat: Dict[str, Any]
    expected_mitigations: List[Dict[str, Any]]


class RiskAssessmentEvaluationRequest(BaseModel):
    """Request model for risk assessment evaluation."""
    threat: Dict[str, Any]
    expected_assessment: Dict[str, Any] 