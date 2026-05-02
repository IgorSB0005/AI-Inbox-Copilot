import os
import json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from schemas import EmailAnalysisRequest, EmailAnalysisResponse

class AIService:
    def __init__(self):
        # Initialize the model with gpt-4o-mini
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        # Use structured output to enforce the response schema
        self.structured_llm = self.llm.with_structured_output(EmailAnalysisResponse)

    def analyze_email(self, request: EmailAnalysisRequest) -> EmailAnalysisResponse:
        # Construct the prompt with Chain of Thought instructions
        prompt_template = PromptTemplate(
            input_variables=["email_body", "user_rules"],
            template=(
                "You are an AI Email Assistant. Your task is to analyze the following email "
                "based on the provided user rules and determine its priority.\n\n"
                "User Rules (JSON Format):\n"
                "{user_rules}\n\n"
                "Email Content:\n"
                "{email_body}\n\n"
                "Instructions:\n"
                "1. Priority Assignment: Determine if the priority is 'high' or 'low' based strictly on the rules.\n"
                "2. Summary: Provide a concise summary of the email.\n"
                "3. Suggested Action: Recommend the next step the user should take.\n"
                "4. Reasoning (Chain of Thought): Think step-by-step about how the user rules "
                "apply to the email content. Identify keywords, sender context, and intent. "
                "Place this ENTIRE step-by-step thinking process into the 'reasoning' field of the output.\n\n"
                "Respond ONLY with the final output matching the required JSON schema."
            )
        )
        
        prompt = prompt_template.format(
            email_body=request.email_body,
            user_rules=json.dumps(request.user_rules, indent=2)
        )
        
        # Invoke the structured LLM which guarantees adherence to EmailAnalysisResponse
        response = self.structured_llm.invoke(prompt)
        return response
