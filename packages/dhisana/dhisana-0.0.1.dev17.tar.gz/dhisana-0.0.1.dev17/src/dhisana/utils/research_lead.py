
# Write up a research summary about the lead using AI. 
# Use the provided user information, ICP to summarize the research

from typing import Dict, List, Optional
from pydantic import BaseModel
from dhisana.utils.assistant_tool_tag import assistant_tool
from dhisana.utils.openai_helpers import get_structured_output_internal    

# Define a model for lead research information
class LeadResearchInformation(BaseModel):
    research_summary: str
    icp_match_score: int

@assistant_tool
async def research_lead_with_ai(user_properties: dict, icp: str, instructions:str, tool_config: Optional[List[Dict]] = None):
    """
    Research on lead provided given input. Check how much it matches ICP.

    This function sends an asynchronous request to gather research information about the lead and evaluate how well it matches the Ideal Customer Profile (ICP).
    
    Parameters:
    user_properties (dict): Information about the lead.
    icp (str): The Ideal Customer Profile description.
    tool_config (Optional[dict]): Configuration for the tool (default is None).

    Returns:
    dict: The JSON response containing the research summary and ICP match score.

    Raises:
    ValueError: If required parameters are missing.
    Exception: If there is an error in processing the request.
    """

    instructions = f"""
    Research the lead based on the following information:
    {user_properties}
    
    Describe how the lead information matches the Ideal Customer Profile (ICP) provided:
    {icp}
    
    Custom insturctions for research
    {instructions}
    
    The output should be in JSON format with the following structure:
    {{
        "research_summary": "Short Summary of the research about lead. Include key insights and findings on how it matches the ICP.",
        "icp_match_score": "Score of how well the lead matches the ICP (0-5). 0 no match, 5 perfect match."
    }}
    """
    response, status = await get_structured_output_internal(instructions, LeadResearchInformation, tool_config=tool_config)
    return response