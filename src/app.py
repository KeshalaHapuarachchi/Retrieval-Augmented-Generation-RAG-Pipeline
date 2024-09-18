from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ticket_analyzer import SupportTicketAnalyzer
from text_cleaning import TextCleaning
import json

app = FastAPI()

#Create an instance of TextCleaning 
text_cleaning_obj = TextCleaning()

# Create an instance of TicketAnalyzer
ticket_analyzer = SupportTicketAnalyzer()

class InputText(BaseModel):
    text: str

@app.post("/analyze_comment/")
async def analyze_comment(comment_input: InputText):
    try:
        cleaned_input = text_cleaning_obj.preprocess_comment(comment_input.text)
        output = ticket_analyzer.analyze_and_respond(cleaned_input)    
        try:
            parsed_json = json.loads(output)
            return parsed_json  
        except json.JSONDecodeError:
            # Handle cases where the response isn't valid JSON
            return {"error": "OpenAI response was not valid JSON."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
