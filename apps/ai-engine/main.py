import os
from fastapi import FastAPI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AI Inbox Copilot - AI Service",
    description="Microservice for processing and prioritizing emails using AI.",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    """
    Basic health check endpoint to verify the service is running.
    """
    return {"status": "healthy"}
