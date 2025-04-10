import os
import requests
from dotenv import load_dotenv


# Environment variables for your WhatsApp Cloud API credentials
WHATSAPP_API_TOKEN = os.getenv("WHATSAPP_API")       # Your permanent or temporary bearer token
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_NO_ID")  # The phone number ID from your WhatsApp app settings

def send_whatsapp_message(recipient_number, message_body):

    """
    Sends a WhatsApp text message using the WhatsApp Cloud API.
    """
    # Construct the API endpoint URL using your phone number ID
    url = f"https://graph.facebook.com/v16.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    
    # Set up the headers with your Bearer token and content type
    headers = {
        "Authorization": f"Bearer {WHATSAPP_API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Build the JSON payload with the required messaging parameters
    data = {
        "messaging_product": "whatsapp",
        "to": recipient_number,  # The recipient's phone number (in international format, no '+' sign)
        "type": "text",
        "text": {
            "body": message_body  # The text content of the message
        }
    }
    
    # (Optional) Print the payload for debugging purposes
    print("Sending payload:", data)
    
    try:
        response = requests.post(url, headers=headers, json=data)
    except Exception as e:
        print(f"An exception occurred while sending the message: {e}")
        return
    
    if response.status_code == 200:
        print("WhatsApp message sent successfully.")
    else:
        print(f"Failed to send message. Status: {response.status_code}, Response: {response.text}")





#     """
#     Sends a WhatsApp text message using the WhatsApp Cloud API.
#     """
#     # Use the environment variable for the phone number ID instead of hardcoding
#     url = f"https://graph.facebook.com/v16.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    
#     headers = {
#         "Authorization": f"Bearer {WHATSAPP_API_TOKEN}",
#         "Content-Type": "application/json"
#     }
    
#     data = {
#         "messaging_product": "whatsapp",
#         "to": recipient_number,    # the number I want to send the message to 
#         "type": "text",
#         "text": {
#             "body": message_body   # What do you want help with today? 
#         }
#     }

#     response = requests.post(url, headers=headers, json=data)
#     if response.status_code == 200:
#         print("WhatsApp message sent successfully.")
#     else:
#         print(f"Failed to send message. Status: {response.status_code}, Response: {response.text}")