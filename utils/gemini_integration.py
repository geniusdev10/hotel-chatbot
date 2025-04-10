# This file contains the function that will take the user request, pass it as a prompt to the gemini module and then return the response of that module. 
import os
import base64
import google.generativeai as genai
from google.generativeai import types
from dotenv import load_dotenv
load_dotenv()


def get_gemini_response(prompt):
        
    client = genai.configure(api_key=os.environ.get("GEMINI_API"))


    model = genai.GenerativeModel('gemini-2.0-flash')    
    
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 1000,
        }
    )
    
    response_text = response.text

    return response_text





# Load environment variables if needed


# def get_gemini_response(prompt):
#     client = genai.Client(api_key=os.environ.get("GEMINI_API"))
#     model = "gemini-2.0-flash"
    
#     # specifies the component of the llm input
#     contents = [
#         types.Content(
#             role="user",
#             parts=[types.Part.from_text(text=prompt)],
#         ),
#     ]
#     generate_content_config = types.GenerateContentConfig(
#         temperature=1,
#         top_p=0.95,
#         top_k=40,
#         max_output_tokens=1000,
#         response_mime_type="text/plain",
#     )
    
#     # string that stores the llm response
#     response_text = ""
#     for chunk in client.models.generate_content_stream(
#         model=model,
#         contents=contents,
#         config=generate_content_config,
#     ):
#         response_text += chunk.text
#     return response_text

# Example testing block (remove or modify when integrating)
if __name__ == "__main__":
    test_prompt = "Tell me about the hotel menu options."
    print("Gemini response:", get_gemini_response(test_prompt))
