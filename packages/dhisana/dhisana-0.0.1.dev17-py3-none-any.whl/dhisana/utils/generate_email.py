# Import necessary modules
import os
from typing import Dict, List, Optional
import aiohttp
from pydantic import BaseModel
from dhisana.utils.assistant_tool_tag import assistant_tool
from dhisana.utils.openai_helpers import get_structured_output_internal    

# Define a model for email copy information
class EmailCopy(BaseModel):
    subject: str
    body: str

@assistant_tool
async def generate_email_copy(user_info: dict, email_template: str, additional_instructions: str, tool_config: Optional[List[Dict]] = None):
    """
    Generate an email copy using the provided user information and email template with placeholders.

    This function sends an asynchronous request to generate an email copy based on the user information and template provided.
    
    Parameters:
    user_info (dict): Information about the user.
    email_template (str): The email template with placeholders.
    additional_instructions (str): Additional instructions for generating the email.
    tool_config (Optional[dict]): Configuration for the tool (default is None).

    Returns:
    dict: The JSON response containing the email subject and body.

    Raises:
    ValueError: If required parameters are missing.
    Exception: If there is an error in processing the request.
    """

    prompt = f"""
    Generate an email copy using the provided user information. The email should follow the given template and fill in the placeholders <<>>.
    
    Email Template:
    {email_template}
    
    Additional Instructions:
    {additional_instructions}
    
    User Information:
    {user_info}
    
    The output should be in JSON format with the following structure:
    {{
        "subject": "Subject of the email.",
        "body": "Body of the email to be sent."
    }}
    """
    response, status = await get_structured_output_internal(prompt, EmailCopy, tool_config=tool_config)
    if status != 'SUCCESS':
        raise Exception("Error in generating the email copy.")
    return response.dict()