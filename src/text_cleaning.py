import re
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import RecognizerResult
from bs4 import BeautifulSoup  

class TextCleaning:
    """A class for text cleaning operations including PII redaction and email thread removal."""
    
    def __init__(self):
        """Initialize Presidio engines for analyzing and anonymizing text."""
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
    
    def redact_pii(self, text):
        """Identifies and redacts PII in the text, except for names."""
        entities = ["CREDIT_CARD", "DATE", "CRYPTO", "DATE_OF_BIRTH", "EMAIL_ADDRESS", 
                    "IBAN_CODE", "IP_ADDRESS", "MEDICAL_LICENSE", "NAME", "NRIC", 
                    "PHONE_NUMBER", "SSN", "SWIFT_CODE", "US_BANK_NUMBER", 
                    "US_ITIN", "US_PASSPORT", 'ADDRESS']
        analyzer_results = self.analyzer.analyze(text=text, entities=entities, language='en')
        redacted_text = self.anonymizer.anonymize(text=text, analyzer_results=analyzer_results)
        return redacted_text.text

    def remove_disclaimer(self, text):
        """Removes common disclaimer patterns from the text."""
        disclaimer_patterns = [
            r'\bDISCLAIMER\b', r'\bdisclaimer\b', r'\bdisclaimer:?\b', 
            r'\bConfidential\b', r'\bCAUTION\b', r'\bcaution\b',
            r'\bWARNING\b', r'\bwarning\b',
            r'The information contained in this email and any attachments',
            r'REPLY ABOVE THIS LINE TO SEND A RESPONSE',
            r'This message is intended for the addressees only',
            r'This email is for the use of the individuals',
            r'Outlook for Android',
            # Add more patterns as needed 
        ]
        for marker in disclaimer_patterns:
            pattern = re.compile(marker, re.IGNORECASE)
            match = pattern.search(text)
            if match:
                text = text[:match.start()]
        return text
    
    @staticmethod
    def extract_text_from_html(html_text):
        """Extracts text content from HTML."""
        soup = BeautifulSoup(html_text, 'html.parser')
        text = soup.get_text(separator="\n", strip=True)
        return text

    @staticmethod
    def replace_emails(text, replacement='[EMAIL]'):
        """Replaces email addresses in the text."""
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        return email_pattern.sub(replacement, text)

    @staticmethod
    def replace_phone_numbers(text, replacement='[PHONE]'):
        """Replaces phone numbers in the text."""
        phone_pattern = re.compile(r'\b(?:\d{3}[-.\s]??\d{3}[-.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-.\s]??\d{4}|\d{3}[-.\s]??\d{4})\b')
        return phone_pattern.sub(replacement, text)

    @staticmethod
    def replace_social_security_numbers(text, replacement='[SSN]'):
        """Replaces social security numbers in the text."""
        ssn_pattern = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
        return ssn_pattern.sub(replacement, text)

    def remove_email_thread(self, email_text):
        """Removes email thread from the email text."""
        thread_patterns = [
            re.compile(r'^-*_*Original Message*-*_*', re.IGNORECASE),  
            re.compile(r'^-*_*Forwarded by', re.IGNORECASE),  
            re.compile(r'From:.*$', re.MULTILINE),  
            re.compile(r'On .* wrote:.*', re.IGNORECASE),  
            re.compile(r'>+.*', re.MULTILINE)  
        ]
        lines = email_text.splitlines()
        split_indices = []
        for i, line in enumerate(lines):
            for pattern in thread_patterns:
                if pattern.match(line):
                    split_indices.append(i)
                    break
        if split_indices:
            first_split = min(split_indices)
            return '\n'.join(lines[:first_split])
        else:
            return email_text
        
    def preprocess_comment(self, comment):
        """Preprocesses the comment by applying PII redaction, disclaimer removal, and email thread removal."""
        processed_comment = self.extract_text_from_html(comment)
        processed_comment = self.redact_pii(processed_comment)
        processed_comment = self.remove_disclaimer(processed_comment)
        processed_comment = self.remove_email_thread(processed_comment)
        return processed_comment
