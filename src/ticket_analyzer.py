import openai

class SupportTicketAnalyzer:
    """Analyzes support ticket comments and provides tailored responses."""

    def __init__(self):
        self.openai_key = 'openai-key'
        self.openai_client = openai.OpenAI(api_key=self.openai_key)
        self.prompt = """You are an intelligent assistant designed to streamline support ticket interactions. Your task is to analyze customer comments on reopened support tickets and categorize them as Actionable or Non-actionable, providing tailored responses for better customer experience.

                            1. Non-actionable Case: In non-actionable cases, the customer expresses gratitude or satisfaction, indicating that no further assistance is required. Check if the customer's comment includes "thank you", "appreciate", "resolved", similar positive sentiment message, expressing gratitude for the assistance received. Examples of non-actionable cases include: 
                               - "Thank you so much for your help!" 
                               - "Thanks for the quick resolution." 
                               - "I appreciate your assistance with this." 
                               - "Great support! Thanks again."

                                If the input customer comments falls into this category return a json with two fields: output and reply 
                                {'output' : 'Non-actionable', 'reply': 'Give a reply according to customer comment.'}

                            2. Actionable Case: In actionable cases, the customer is seeking additional information or not happy with agents resolution or awaiting for a reply from the support agent. Verify if the customer's comment is a genuine inquiry or concern related to their problem, indicating dissatisfaction or unresolved issues. Examples of Actionable cases include: 
                               - "I'm still having trouble with this. Can you please take another look?" 
                               - "Unfortunately, this solution didn't work. Do you have other suggestions?" 
                               - "Thanks for trying, but I think the issue might be more complicated." 
                               - "I appreciate the help, but I need more information to fix this myself." 

                               Return a JSON with these fields: 
                               {'output': 'Actionable', 'reply': 'Provide a reply according to the customer comment.'}

                            Identify the below given comment and return an output JSON with 'output' and 'reply':
                            Input Customer Comment:\n 
                        """

    def analyze_and_respond(self, comment):
        """Analyzes a support ticket comment and generates a response.

        Args:
            comment (str): The customer's comment on the reopened ticket.

        Returns:
            dict: A JSON-style dictionary with the following keys:
                * 'output': 'Actionable' or 'Non-actionable'
                * 'reply': A tailored response to the customer's comment.
        """

        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": self.prompt + comment}]
        )

        output_json = response.choices[0].message.content.strip()  # Assuming clean JSON output
        return output_json