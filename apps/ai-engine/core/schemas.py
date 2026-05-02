from pydantic import BaseModel, Field
from typing import Dict, Any, Literal, List

class EmailAnalysisRequest(BaseModel):
    email_body: str = Field(..., description="The raw text content of the email.")
    user_rules: Dict[str, Any] = Field(
        default_factory=dict, 
        description="JSON object containing user-defined rules for prioritizing and categorizing emails."
    )

class EmailAnalysisResponse(BaseModel):
    priority: Literal["high", "low"] = Field(..., description="The priority of the email based on the rules.")
    summary: str = Field(..., description="A concise summary of the email content.")
    suggested_action: str = Field(..., description="A suggested action for the user to take regarding the email.")
    reasoning: str = Field(..., description="The reasoning behind the priority and suggested action.")

class ProcessInboxRequest(BaseModel):
    gmail_address: str = Field(..., description="The Gmail address to scrape.")
    app_password: str = Field(..., description="The Gmail App Password.")
    user_rules: Dict[str, Any] = Field(
        default_factory=dict,
        description="JSON object containing user-defined rules."
    )

class ProcessedEmail(BaseModel):
    subject: str
    sender: str
    analysis: EmailAnalysisResponse

class ProcessInboxResponse(BaseModel):
    processed_emails: List[ProcessedEmail] = Field(..., description="A list of processed emails with their AI analysis.")
