# Check validity of email

import os
import os
from typing import Dict, List, Optional
import aiohttp
from dhisana.utils.assistant_tool_tag import assistant_tool    
# Use Zero Bounce to check email validity.

# Get Private API Key from Tool Configuration
def get_zero_bounce_access_token(tool_config: Optional[List[Dict]] = None) -> str:
    """
    Retrieves the ZeroBounce access token from the provided tool configuration.

    Args:
        tool_config (list): A list of dictionaries containing the tool configuration. 
                            Each dictionary should have a "name" key and a "configuration" key,
                            where "configuration" is a list of dictionaries containing "name" and "value" keys.

    Returns:
        str: The ZeroBounce access token.

    Raises:
        ValueError: If the access token is not found in the tool configuration or environment variable.
    """
    if tool_config:
        zerobounce_config = next(
            (item for item in tool_config if item.get("name") == "zerobounce"), None
        )
        if zerobounce_config:
            config_map = {
                item["name"]: item["value"]
                for item in zerobounce_config.get("configuration", [])
                if item
            }
            ZERO_BOUNCE_API_KEY = config_map.get("apiKey")
        else:
            ZERO_BOUNCE_API_KEY = None
    else:
        ZERO_BOUNCE_API_KEY = None

    ZERO_BOUNCE_API_KEY = ZERO_BOUNCE_API_KEY or os.getenv("ZERO_BOUNCE_API_KEY")
    if not ZERO_BOUNCE_API_KEY:
        raise ValueError("ZERO_BOUNCE_API_KEY access token not found in tool_config or environment variable")
    return ZERO_BOUNCE_API_KEY

@assistant_tool
async def check_email_validity_with_zero_bounce(email_id: str, tool_config: Optional[List[Dict]] = None):
    """
    Validate a single email address using the ZeroBounce API.

    This function sends an asynchronous GET request to the ZeroBounce API to validate the provided email address.
    
    Parameters:
    email_id (str): The email address to be validated.

    Returns:
    dict: The JSON response from the ZeroBounce API containing the validation results.

    Raises:
    ValueError: If the ZeroBounce API key is not found in the environment variables.
    Exception: If the response status code from the ZeroBounce API is not 200.
    """
    ZERO_BOUNCE_API_KEY = get_zero_bounce_access_token(tool_config)

    url = f"https://api.zerobounce.net/v2/validate?api_key={ZERO_BOUNCE_API_KEY}&email={email_id}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(f"Error: Received status code {response.status}")
            result = await response.json()
            return result