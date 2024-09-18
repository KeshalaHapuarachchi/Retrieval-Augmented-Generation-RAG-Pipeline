# ThankYou GPT

Support Ticket Analyzer is a tool designed to streamline support ticket interactions. It analyzes customer comments on reopened support tickets and categorizes them as Actionable or Non-actionable, providing tailored responses for better customer experience.

## Overview

This project consists of three main components:
1. **Text Cleaning**: A module responsible for preprocessing customer comments by performing tasks such as PII redaction, disclaimer removal, and email thread removal.
2. **GPT Call**: A module responsible for making calls to the OpenAI API to generate responses using the GPT model based on input text.
3. **FastAPI**: A web application built with FastAPI that provides an API endpoint for analyzing customer comments.

## Prerequisites

* Python 3.7+
* An OpenAI API Key (https://beta.openai.com/account/api-keys)

## Installation*

1. Clone this repository:
   ```bash
      git clone [invalid URL removed]
   ```
2. Create a virtual environment and activate it:
    ```python -m venv env
       source env/bin/activate
    ```
3. Install dependencies:
    ```pip install -r requirements.txt
    ```
    
## Usage

1. Run the FastAPI application:

    ```uvicorn main:app --host <ip_address> --port <port_number> --reload
    ```

2. Send POST requests to the `/analyze_comment/` endpoint with JSON body containing the customer comment:
    ```json
    {
        "text": "Customer comment goes here"
    }
    ```

