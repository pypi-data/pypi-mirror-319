import os
from typing import Dict, List, Optional
import aiohttp
from dhisana.utils.apollo_tools import enrich_person_info_from_apollo
from dhisana.utils.assistant_tool_tag import assistant_tool    
from pydantic import BaseModel

# Check if the given LinkedIn Url is valid and matches the input record.

class LeadLinkedInMatch(BaseModel):
    first_name_matched: bool = False
    last_name_matched: bool = False
    linkedin_url_valid: bool = False
    title_matched: bool = False
    location_matched: bool = False


@assistant_tool
async def check_linkedin_url_validity_with_apollo(user_properties: dict, tool_config: Optional[List[Dict]] = None) -> LeadLinkedInMatch:
    """
    Validates the LinkedIn URL and user information using the Apollo API.

    Args:
        user_properties (dict): A dictionary containing user properties such as 'first_name', 'last_name', 'title', 'location', and 'user_linkedin_url'.
        tool_config (Optional[dict]): A dictionary containing the tool configuration. Expected to have a "configuration" key which maps to a list of dictionaries, each containing "name" and "value" keys.

    Returns:
        LeadLinkedInMatch: An object indicating whether the LinkedIn URL and user information match the data from Apollo.

    Raises:
        ValueError: If the access token is not found in the tool configuration or environment variable.
    """
    linkedin_url = user_properties.get('user_linkedin_url', "")
    lead_matched = LeadLinkedInMatch()

    linkedin_data = await enrich_person_info_from_apollo(linkedin_url=linkedin_url, tool_config=tool_config)
    if not linkedin_data:
        return lead_matched

    person_data = linkedin_data.get('person', {})

    if user_properties.get('first_name', ""):
        lead_matched.first_name_matched = person_data.get('first_name') == user_properties.get('first_name')
    else:
        lead_matched.first_name_matched = True

    if user_properties.get('last_name', ""):
        lead_matched.last_name_matched = person_data.get('last_name') == user_properties.get('last_name')
    else:
        lead_matched.last_name_matched = True

    if user_properties.get('title', ""):
        lead_matched.title_matched = person_data.get('title') == user_properties.get('title')
    else:
        lead_matched.title_matched = True

    if user_properties.get('location', ""):
        lead_matched.location_matched = person_data.get('location') == user_properties.get('location')
    else:
        lead_matched.location_matched = True

    lead_matched.linkedin_url_valid = True
    return lead_matched