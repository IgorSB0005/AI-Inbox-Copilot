import os
from fastapi import FastAPI
from dotenv import load_dotenv

from schemas import EmailAnalysisRequest, EmailAnalysisResponse
from service import AIService

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI Inbox Copilot - AI Service",
    description="Microservice for processing and prioritizing emails using AI.",
    version="1.0.0"
)

# Initialize the AI Service
ai_service = AIService()

@app.get("/health")
def health_check():
    """
    Basic health check endpoint to verify the service is running.
    """
    return {"status": "healthy"}

@app.post("/api/v1/analyze", response_model=EmailAnalysisResponse)
def analyze_email_endpoint(request: EmailAnalysisRequest):
    """
    Analyze an email body against user rules and return structured priorities/summaries.
    """
    return ai_service.analyze_email(request)
