import os
from fastapi import FastAPI
from dotenv import load_dotenv

from core.schemas import EmailAnalysisRequest, EmailAnalysisResponse, ProcessInboxRequest, ProcessInboxResponse, ProcessedEmail
from ai.service import AIService
from scraper.imap_client import GmailScraper
from scraper.text_cleaner import clean_email_body

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
    Analyze a single email body against user rules and return structured priorities/summaries.
    """
    return ai_service.analyze_email(request)

@app.post("/api/v1/process", response_model=ProcessInboxResponse)
def process_inbox_endpoint(request: ProcessInboxRequest):
    """
    Ingest emails from Gmail using IMAP, clean the HTML, and run them through the AI for prioritization.
    """
    scraper = GmailScraper(email=request.gmail_address, app_password=request.app_password)
    
    try:
        unread_emails = scraper.fetch_unread_emails()
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=f"Failed to fetch emails: {str(e)}")
        
    processed_emails = []
    
    for email_data in unread_emails:
        # Clean the HTML to prepare for LLM context
        clean_text = clean_email_body(email_data["raw_body"])
        
        # Prepare request for AI Service
        ai_request = EmailAnalysisRequest(
            email_body=f"Subject: {email_data['subject']}\nSender: {email_data['sender']}\n\n{clean_text}",
            user_rules=request.user_rules
        )
        
        # Analyze using LLM
        analysis = ai_service.analyze_email(ai_request)
        
        processed_emails.append(ProcessedEmail(
            subject=email_data["subject"],
            sender=email_data["sender"],
            analysis=analysis
        ))
        
    return ProcessInboxResponse(processed_emails=processed_emails)
