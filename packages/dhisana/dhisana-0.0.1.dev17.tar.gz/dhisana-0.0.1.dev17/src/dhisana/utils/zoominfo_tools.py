import asyncio
import hashlib
import json
import logging
import os
import aiohttp
import backoff
from typing import Dict, List, Optional, Tuple

from dhisana.utils.cache_output_tools import cache_output, retrieve_output
from dhisana.utils.assistant_tool_tag import assistant_tool

def get_zoominfo_credentials_from_config(
    tool_config: Optional[List[Dict]] = None
) -> Tuple[Optional[str], Optional[str]]:
    """
    Retrieve ZoomInfo API key and secret from tool_config (looking for 'name' == 'zoominfo'),
    or fall back to environment variables if not found.

    Args:
        tool_config: Optional config containing ZoomInfo credentials.

    Returns:
        Tuple (zoominfo_api_key, zoominfo_api_secret)
    """
    zoominfo_api_key = None
    zoominfo_api_secret = None

    if tool_config:
        zoominfo_config = next(
            (item for item in tool_config if item.get("name") == "zoominfo"), None
        )
        if zoominfo_config:
            # Convert the list of dicts under 'configuration' to a simple map {name: value}
            config_map = {
                cfg["name"]: cfg["value"]
                for cfg in zoominfo_config.get("configuration", [])
                if cfg
            }
            zoominfo_api_key = config_map.get("apiKey")
            zoominfo_api_secret = config_map.get("apiSecret")

    # Fallback to environment variables if not found in tool_config
    zoominfo_api_key = zoominfo_api_key or os.environ.get("ZOOMINFO_API_KEY")
    zoominfo_api_secret = zoominfo_api_secret or os.environ.get("ZOOMINFO_API_SECRET")

    return zoominfo_api_key, zoominfo_api_secret


@backoff.on_exception(
    backoff.expo,
    (aiohttp.ClientResponseError, Exception),
    max_tries=3,
    giveup=lambda e: not (isinstance(e, aiohttp.ClientResponseError) and e.status == 429),
    factor=2,
)
async def get_zoominfo_access_token(tool_config: Optional[List[Dict]] = None) -> str:
    """
    Obtain a ZoomInfo access token, using credentials from the provided tool_config or
    environment variables.

    Args:
        tool_config: Optional config containing ZoomInfo credentials.

    Returns:
        The ZoomInfo JWT access token.

    Raises:
        EnvironmentError: If the necessary credentials are missing.
        Exception: If the ZoomInfo API authentication fails.
    """
    zoominfo_api_key, zoominfo_api_secret = get_zoominfo_credentials_from_config(tool_config)

    if not zoominfo_api_key or not zoominfo_api_secret:
        raise EnvironmentError(
            "ZoomInfo API key and secret not found in tool_config or environment variables"
        )

    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "username": zoominfo_api_key,
        "password": zoominfo_api_secret
    }
    url = "https://api.zoominfo.com/authenticate"

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                result = await response.json()
                return result.get("accessToken")
            else:
                result = await response.json()
                raise Exception(f"Failed to authenticate with ZoomInfo API: {result}")


@assistant_tool
@backoff.on_exception(
    backoff.expo,
    (aiohttp.ClientResponseError, Exception),
    max_tries=3,
    giveup=lambda e: not (isinstance(e, aiohttp.ClientResponseError) and e.status == 429),
    factor=2,
)
async def enrich_person_info_from_zoominfo(
    linkedin_url: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    tool_config: Optional[List[Dict]] = None
) -> dict:
    """
    Fetch a person's details from ZoomInfo using LinkedIn URL, email, or phone number.

    Parameters:
    - linkedin_url (str, optional): LinkedIn profile URL of the person.
    - email (str, optional): Email address of the person.
    - phone (str, optional): Phone number of the person.
    - tool_config (list of dict, optional): Config containing ZoomInfo credentials.

    Returns:
    - dict: JSON response containing person information.
    """
    access_token = await get_zoominfo_access_token(tool_config)
    if not access_token:
        return {"error": "Failed to obtain ZoomInfo access token"}

    if not linkedin_url and not email and not phone:
        return {"error": "At least one of linkedin_url, email, or phone must be provided"}

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    data = {}
    cache_key_value = None

    # Build request and check cache
    if linkedin_url:
        data["personLinkedinUrls"] = [linkedin_url]
        cache_key_value = linkedin_url
    if email:
        data["personEmails"] = [email]
    if phone:
        data["personPhones"] = [phone]

    # If a LinkedIn URL is provided, attempt to retrieve from cache
    if cache_key_value:
        cached_response = retrieve_output("enrich_person_info_from_zoominfo", cache_key_value)
        if cached_response is not None:
            return cached_response

    url = "https://api.zoominfo.com/person/contact"

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                result = await response.json()
                # Cache if LinkedIn URL was used
                if cache_key_value:
                    cache_output("enrich_person_info_from_zoominfo", cache_key_value, result)
                return result
            elif response.status == 429:
                logging.warning("enrich_person_info_from_zoominfo Rate limit hit")
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message="Rate limit exceeded",
                    headers=response.headers
                )
            else:
                result = await response.json()
                logging.warning(
                    f"enrich_person_info_from_zoominfo failed with status {response.status}: {result}"
                )
                return {"error": result}


@assistant_tool
@backoff.on_exception(
    backoff.expo,
    (aiohttp.ClientResponseError, Exception),
    max_tries=3,
    giveup=lambda e: not (isinstance(e, aiohttp.ClientResponseError) and e.status == 429),
    factor=2,
)
async def enrich_organization_info_from_zoominfo(
    organization_domain: Optional[str] = None,
    tool_config: Optional[List[Dict]] = None
) -> dict:
    """
    Fetch an organization's details from ZoomInfo using the organization domain.

    Parameters:
    - organization_domain (str, optional): Domain of the organization.
    - tool_config (list of dict, optional): Config containing ZoomInfo credentials.

    Returns:
    - dict: JSON response containing organization information.
    """
    access_token = await get_zoominfo_access_token(tool_config)
    if not access_token:
        return {"error": "Failed to obtain ZoomInfo access token"}

    if not organization_domain:
        return {"error": "Organization domain must be provided"}

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    cached_response = retrieve_output("enrich_organization_info_from_zoominfo", organization_domain)
    if cached_response is not None:
        return cached_response

    data = {
        "companyDomains": [organization_domain]
    }

    url = "https://api.zoominfo.com/company/enrich"

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                result = await response.json()
                cache_output("enrich_organization_info_from_zoominfo", organization_domain, result)
                return result
            elif response.status == 429:
                logging.warning("enrich_organization_info_from_zoominfo Rate limit hit")
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message="Rate limit exceeded",
                    headers=response.headers
                )
            else:
                result = await response.json()
                logging.warning(
                    f"enrich_organization_info_from_zoominfo failed with status {response.status}: {result}"
                )
                return {"error": result}


@assistant_tool
async def get_enriched_customer_information_with_zoominfo(
    linkedin_url: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
    required_fields: Optional[List[str]] = None,
    data_sources: Optional[List[str]] = None,
    tool_config: Optional[List[Dict]] = None
) -> dict:
    """
    Fetch a person's details from specified data sources using LinkedIn URL, email, or phone number.

    Parameters:
    - linkedin_url (str, optional): LinkedIn profile URL of the person.
    - email (str, optional): Email address of the person.
    - phone (str, optional): Phone number of the person.
    - required_fields (list of str, optional): Properties of the customer to fetch.
    - data_sources (list of str, optional): Data sources to fetch from. Defaults to all sources.
    - tool_config (list of dict, optional): Config containing ZoomInfo credentials.

    Returns:
    - dict: JSON response containing person information.
    """
    # Set default values if not provided
    if required_fields is None:
        required_fields = [
            "job_history",
            "education_history",
            "skills",
            "headline",
            "summary",
            "experiences",
            "projects",
            "certifications",
            "publications",
            "languages",
            "volunteer_work",
        ]
    if data_sources is None:
        data_sources = ["zoominfo", "websearch", "linkedin"]

    # ZoomInfo fetch
    data = await enrich_person_info_from_zoominfo(
        linkedin_url=linkedin_url,
        email=email,
        phone=phone,
        tool_config=tool_config,
    )
    return data


@assistant_tool
async def get_enriched_organization_information_with_zoominfo(
    organization_domain: Optional[str] = None,
    required_fields: Optional[List[str]] = None,
    data_sources: Optional[List[str]] = None,
    tool_config: Optional[List[Dict]] = None
) -> dict:
    """
    Fetch an organization's details from specified data sources using the organization domain.

    Parameters:
    - organization_domain (str, optional): Domain of the organization.
    - required_fields (list of str, optional): Properties of the organization to fetch.
    - data_sources (list of str, optional): Data sources to fetch from. Defaults to all sources.
    - tool_config (list of dict, optional): Config containing ZoomInfo credentials.

    Returns:
    - dict: JSON response containing organization information.
    """
    data = await enrich_organization_info_from_zoominfo(
        organization_domain=organization_domain,
        tool_config=tool_config,
    )
    return data


@backoff.on_exception(
    backoff.expo,
    (aiohttp.ClientResponseError, Exception),
    max_tries=5,
    giveup=lambda e: not (isinstance(e, aiohttp.ClientResponseError) and e.status == 429),
    factor=2,
)
async def fetch_zoominfo_data(
    session: aiohttp.ClientSession,
    url: str,
    headers: Dict[str, str],
    payload: dict
) -> dict:
    """
    Helper function to handle ZoomInfo API calls with caching.

    Args:
        session: Aiohttp ClientSession.
        url: The ZoomInfo API endpoint URL.
        headers: Request headers, including Authorization.
        payload: JSON payload for POST request.

    Returns:
        The JSON data from ZoomInfo, or raises an exception on error.
    """
    key_data = f"{url}_{json.dumps(payload, sort_keys=True)}"
    key_hash = hashlib.sha256(key_data.encode()).hexdigest()
    cached_response = retrieve_output("fetch_zoominfo_data", key_hash)
    if cached_response is not None:
        return cached_response

    async with session.post(url, headers=headers, json=payload) as response:
        if response.status == 200:
            result = await response.json()
            cache_output("fetch_zoominfo_data", key_hash, result)
            return result
        elif response.status == 429:
            raise aiohttp.ClientResponseError(
                request_info=response.request_info,
                history=response.history,
                status=response.status,
                message="Rate limit exceeded",
                headers=response.headers
            )
        else:
            response.raise_for_status()


@assistant_tool
async def search_recent_job_changes_with_zoominfo(
    job_titles: List[str],
    locations: List[str],
    organization_num_employees_ranges: Optional[List[str]],
    max_items_to_return: int,
    tool_config: Optional[List[Dict]] = None
) -> List[dict]:
    """
    Search for individuals with specified job titles, locations, and optionally organization
    employee ranges who have recently changed jobs.

    Parameters:
    - job_titles (List[str]): List of job titles to search for.
    - locations (List[str]): List of locations to search in.
    - organization_num_employees_ranges (List[str], optional): Filter by organization size range.
    - max_items_to_return (int): Maximum number of items to return (1-5000).
    - tool_config (list of dict, optional): Config containing ZoomInfo credentials.

    Returns:
    - List[dict]: A list of individuals matching the criteria or error details.
    """
    access_token = await get_zoominfo_access_token(tool_config)
    if not access_token:
        raise EnvironmentError("Failed to obtain ZoomInfo access token")

    if max_items_to_return <= 0:
        max_items_to_return = 10
    elif max_items_to_return > 5000:
        max_items_to_return = 5000

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    url = "https://api.zoominfo.com/person/search"

    # Define search criteria
    criteria = {
        "personTitles": job_titles,
        "personLocationCities": locations,
        "pageSize": min(max_items_to_return, 100),
        "sortBy": "LastUpdatedDate",
        "sortOrder": "DESC"
    }

    if organization_num_employees_ranges:
        criteria["companyEmployeeCountRanges"] = organization_num_employees_ranges

    async with aiohttp.ClientSession() as session:
        results = []
        page = 1
        page_size = min(max_items_to_return, 100)

        while len(results) < max_items_to_return:
            payload = {
                "criteria": criteria,
                "pagination": {
                    "page": page,
                    "pageSize": page_size
                }
            }

            try:
                data = await fetch_zoominfo_data(session, url, headers, payload)
                contacts = data.get("data", [])
                if not contacts:
                    break
                results.extend(contacts)

                total_records = data.get("total", 0)
                total_pages = (total_records // page_size) + (1 if total_records % page_size else 0)

                if page >= total_pages:
                    break

                page += 1
            except aiohttp.ClientResponseError as e:
                if e.status == 429:
                    # Rate limit: backoff will retry
                    await asyncio.sleep(30)
                else:
                    # Return error details as a JSON string in a list
                    error_details = {
                        "status": e.status,
                        "message": str(e),
                        "url": str(e.request_info.url),
                        "headers": dict(e.headers),
                    }
                    error_json = json.dumps(error_details)
                    return [error_json]

        return results[:max_items_to_return]


@assistant_tool
async def get_organization_details_from_zoominfo(
    organization_id: str,
    tool_config: Optional[List[Dict]] = None
) -> dict:
    """
    Fetch an organization's details from ZoomInfo using the organization ID.

    Parameters:
    - organization_id (str): ID of the organization.
    - tool_config (list of dict, optional): Config containing ZoomInfo credentials.

    Returns:
    - dict: Organization details or an error message.
    """
    access_token = await get_zoominfo_access_token(tool_config)
    if not access_token:
        return {"error": "Failed to obtain ZoomInfo access token"}

    if not organization_id:
        return {"error": "Organization ID must be provided"}

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    cached_response = retrieve_output("get_organization_details_from_zoominfo", organization_id)
    if cached_response is not None:
        return cached_response

    url = "https://api.zoominfo.com/company/detail"
    data = {"companyId": organization_id}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                result = await response.json()
                org_details = result.get("data", {})
                if org_details:
                    cache_output("get_organization_details_from_zoominfo", organization_id, org_details)
                    return org_details
                else:
                    return {"error": "Organization details not found in the response"}
            elif response.status == 429:
                logging.warning("get_organization_details_from_zoominfo Rate limit hit")
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status,
                    message="Rate limit exceeded",
                    headers=response.headers
                )
            else:
                result = await response.json()
                return {"error": result}


@assistant_tool
async def get_organization_domain_from_zoominfo(
    organization_id: str,
    tool_config: Optional[List[Dict]] = None
) -> dict:
    """
    Fetch an organization's domain from ZoomInfo using the organization ID.

    Parameters:
    - organization_id (str): ID of the organization.
    - tool_config (list of dict, optional): Config containing ZoomInfo credentials.

    Returns:
    - dict: Contains the organization's ID and domain, or an error message.
    """
    result = await get_organization_details_from_zoominfo(organization_id, tool_config=tool_config)
    if "error" in result:
        return result

    domain = result.get("companyWebsite")
    if domain:
        return {"organization_id": organization_id, "domain": domain}
    else:
        return {"error": "Domain not found in the organization details"}
