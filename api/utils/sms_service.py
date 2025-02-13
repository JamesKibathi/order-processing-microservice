import africastalking


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













