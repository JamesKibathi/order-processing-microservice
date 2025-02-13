import africastalking

from django.core.mail import send_mail
from django.conf import settings


import os
from dotenv import load_dotenv
load_dotenv()


username = os.getenv('AT_USERNAME') 
api_key =os.getenv('AT_API_KEY')


africastalking.initialize(username, api_key)

class SendSMS:
    def __init__(self):
        self.sms = africastalking.SMS

    def send(self, message, recipients):
        sender = os.getenv('AT_SHORT_CODE') 
        try:
            response = self.sms.send(message, recipients, sender)
            print (response)
            return response  
        except Exception as e:
            print (f'Houston, we have a problem: {e}')
            return {'error': str(e)}   
        

# sms_service = SendSMS()
# response = sms_service.send("Hello, Django!", ["+254706929499"])
# print(response)


class EmailService:
    def __init__(self):
        """Initialize EmailService with default sender email."""
        self.default_from_email = settings.DEFAULT_FROM_EMAIL

    def send_email(self, subject, message, recipient_list, from_email=None):
        """Send an email with the given subject and message."""
        if not from_email:
            from_email = self.default_from_email  
        
        if not isinstance(recipient_list, list):
            recipient_list = [recipient_list]  
        
        try:
            response = send_mail(subject, message, from_email, recipient_list)
            print(f"Email sent successfully to {recipient_list}")
            print("Response ...",response)
            return {'status': 'success', 'message': f'Email sent to {recipient_list}'}
        except Exception as e:
            print(f"Email sending failed: {e}")
            return {'status': 'error', 'message': str(e)}
        
# email_service = EmailService()
# response=email_service.send_email("New Order", "Hey James, Your Order has been processed", ["njenga.consulting@gmail.com"])   

# print("Email Response ...",response)