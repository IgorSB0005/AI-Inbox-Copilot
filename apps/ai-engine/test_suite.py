import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

# Mock data for tests
MOCK_RULES = {
    "high_priority_keywords": ["urgent", "outage", "asap", "client"],
    "spam_senders": ["promo@spammer.com", "newsletter@updates.com"],
    "ignore_subjects": ["weekly update", "newsletter"]
}

EMAIL_SPAM = {
    "email_body": "From: promo@spammer.com\nSubject: You won a free iPhone!\n\nClick here to claim your prize.",
    "user_rules": MOCK_RULES
}

EMAIL_URGENT = {
    "email_body": "From: boss@company.com\nSubject: URGENT: System Outage\n\nThe production database is down. We need this fixed ASAP.",
    "user_rules": MOCK_RULES
}

EMAIL_NEWSLETTER = {
    "email_body": "From: newsletter@updates.com\nSubject: Weekly Update: Tech News\n\nHere are the top tech stories for this week.",
    "user_rules": MOCK_RULES
}

# Note: These tests require a valid OPENAI_API_KEY in the environment to run the actual model.
# In a real CI environment, we would mock the AIService or ChatOpenAI call.

@pytest.mark.skipif("OPENAI_API_KEY" not in os.environ, reason="OpenAI API Key not set")
def test_analyze_urgent_email():
    response = client.post("/api/v1/analyze", json=EMAIL_URGENT)
    assert response.status_code == 200
    data = response.json()
    assert data["priority"] == "high"
    assert "reasoning" in data
    assert len(data["reasoning"]) > 0

@pytest.mark.skipif("OPENAI_API_KEY" not in os.environ, reason="OpenAI API Key not set")
def test_analyze_spam_email():
    response = client.post("/api/v1/analyze", json=EMAIL_SPAM)
    assert response.status_code == 200
    data = response.json()
    assert data["priority"] == "low"
    assert "reasoning" in data

@pytest.mark.skipif("OPENAI_API_KEY" not in os.environ, reason="OpenAI API Key not set")
def test_analyze_newsletter_email():
    response = client.post("/api/v1/analyze", json=EMAIL_NEWSLETTER)
    assert response.status_code == 200
    data = response.json()
    assert data["priority"] == "low"
    assert "reasoning" in data
