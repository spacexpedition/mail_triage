from pydantic import Field, BaseModel
from typing import Optional, List, Dict
from openenv.core.env_server import Action, Observation

class URLInfo(BaseModel):
    url:str
    is_shortened: bool
    domain_age_days: int
    has_ssl: bool
    reputation_score: float # 0.0 (Malicious) to 1.0 (Safe)

class MyEnvV4Observation(Observation):
    """Enhanced Observation Space for the Security Agent."""
    sender: str
    subject: str
    body: str
    raw_headers: str
    hop_count: int
    auth_results: Dict[str, str] # e.g., {"SPF": "pass", "DKIM": "fail"}
    urls: List[URLInfo]
    echoed_message: str = ""

class MyEnvV4Action(Action):
    """Enhanced Action Space with Explainability."""
    message: str = Field(..., description="Classification: 'INBOX', 'SPAM', or 'QUARANTINE'")
    reasoning: str = Field(..., description="Justification for the triage decision (e.g., 'Suspicious URL and failed SPF')")