import asyncio
import csv
import os
from typing import List, Dict, Optional
import aiofiles
import tldextract

from dhisana.utils.apollo_tools import enrich_person_info_from_apollo
from dhisana.utils.assistant_tool_tag import assistant_tool
from dhisana.utils.serpapi_search_tools import (
    find_company_linkedin_url_with_google_search,
    find_user_linkedin_url_google,
    get_company_domain_from_google_search,
    find_user_linkedin_url_by_job_title_google,
    get_company_website_from_linkedin_url
)

# Function to enrhich lead information 
# Given only company name, it will find the company linkedin url and website.
# Given only user name, title, location, and company name, it will find the user linkedin url.
# This can be enhanced to checked from multiple sources like proxycurl, apollo, zoomInfo, clearbit etc to be more robust.
# TODO: Add enrichment for email and mobile number also.

@assistant_tool
async def enrich_lead_information(user_properties: dict, tool_config: Optional[List[Dict]] = None):
    """
    Enrich lead information including company details, linked in url.
    Use multiple tools like Google Custom Search, Apollo API to enrich the data.

    Args:
        user_properties (dict): A dictionary containing user properties such as 'first_name', 'last_name', 'title', 'location', and 'user_linkedin_url'.
        tool_config (Optional[dict]): A dictionary containing the tool configuration. Expected to have a "configuration" key which maps to a list of dictionaries, each containing "name" and "value" keys.

    Returns:
        user_properties: Enriched lead informtion.

    Raises:
        ValueError: If the access token is not found in the tool configuration or environment variable.
    """
    
    # Enrich the organization or company information
    await enrich_organization_information(user_properties, tool_config=tool_config)
    
    # Enrich user linkedin url
    user_linkedin_url = user_properties.get("user_linkedin_url", "").strip()
    user_properties['linkedin_url_match'] = False
    if not user_linkedin_url:
        #TODO: Make this more robust by double checking company, location etc.
        name = user_properties.get("first_name", "").strip() + ' ' + user_properties.get("last_name", "").strip()
        title = user_properties.get("title", "CXO")
        location = user_properties.get("location", "US")
        org_name = user_properties.get("organization_name", "").strip()
        user_linkedin_url = await find_user_linkedin_url_google(user_name=name, user_title=title, user_location=location, user_company=org_name, tool_config=tool_config)
        user_properties["user_linkedin_url"] = user_linkedin_url
                    
    linkedin_url = user_properties.get('user_linkedin_url', "")

    # Get User data using linked in URL
    linkedin_data = await enrich_person_info_from_apollo(linkedin_url=linkedin_url, tool_config=tool_config)
    if not linkedin_data:
        return user_properties
    
    person_data = linkedin_data.get('person', {})
    user_properties['lead_linkedin_data'] = person_data
    if not user_properties.get('email', ""):
        user_properties['email'] = person_data.get('email', "")
    if not user_properties.get('phone', ""):
        user_properties['phone'] = person_data.get("contact").get("sanitized_phone")
            
    first_name_matched = False
    last_name_matched = False

    if user_properties.get('first_name', ""):
        first_name_matched = person_data.get('first_name') == user_properties.get('first_name')

    if user_properties.get('last_name', ""):
        last_name_matched = person_data.get('last_name') == user_properties.get('last_name')
        
    if first_name_matched and last_name_matched:
        user_properties['linkedin_url_match'] = True
       
    return user_properties

# Linked in website sometimes have indirect links. Need to validate company domain from multiple sources.
EXCLUDED_LINK_DOMAINS = [
    "beacon.ai",
    "tap.bio",
    "campsite.bio",
    "shor.by",
    "milkshake.app",
    "lnk.bio",
    "carrd.co",
    "bio.fm",
    "withkoji.com",
    "flowcode.com",
    "biolinky.co",
    "contactinbio.com",
    "linktr.ee",
    "linkedin.com",
    "facebook.com",
    "youtube.com"
]


def get_domain_from_website(website: str) -> str:
    """
    Extracts the domain from a given website URL using tldextract.
    Returns an empty string if no website is provided.
    """
    if not website:
        return ""
    extracted = tldextract.extract(website)
    domain = f"{extracted.domain}.{extracted.suffix}"
    return domain


def is_excluded_domain(domain: str) -> bool:
    """
    Checks if the domain is in the EXCLUDED_LINK_DOMAINS list.
    """
    return domain in EXCLUDED_LINK_DOMAINS


async def enrich_organization_info_from_name(row: Dict[str, str], tool_config: Optional[List[Dict]] = None) -> None:
    """
    Given a CSV row containing 'organization_name', 'company_linkedin_url', and 'website' keys,
    attempts to enrich the row with a primary domain and valid website.
    """
    org_name_key = "organization_name"
    org_domain_key = "primary_domain_of_organization"
    linkedin_url_key = "company_linkedin_url"
    website_key = "website"

    company_location = "US"

    org_name = row.get(org_name_key, "").strip()
    if org_name.lower() in ["none", "freelance"]:
        row[org_name_key] = ""
        org_name = ""

    if not org_name:
        return

    linkedin_url = row.get(linkedin_url_key, "").strip()
    if not linkedin_url:
        linkedin_url = await find_company_linkedin_url_with_google_search(org_name, company_location=company_location, tool_config=tool_config)
    if linkedin_url:
        # If we already have a LinkedIn URL, try extracting the company website from it
        row[linkedin_url_key] = linkedin_url
        company_website = await get_company_website_from_linkedin_url(linkedin_url)
        domain = get_domain_from_website(company_website)
        # If the domain is excluded, then try to fetch a domain from Google Search
        if is_excluded_domain(domain):
            domain = await get_company_domain_from_google_search(org_name, company_location, tool_config=tool_config)
        row[org_domain_key] = domain or ""
        if domain:
            row[website_key] = company_website
        else:
            row[website_key] = ""
    else:
        # No LinkedIn URL - we can't do much else in this snippet
        row[org_domain_key] = ""


async def enrich_organization_information(row: Dict[str, str], tool_config: Optional[List[Dict]] = None) -> None:
    """
    Enriches a CSV row's organization-related data if organization_name is present.
    """
    org_name_key = "organization_name"
    org_name = row.get(org_name_key, "").strip()

    # If the org name is 'none' or 'freelance', treat it as empty
    if org_name.lower() in ["none", "freelance"]:
        row[org_name_key] = ""
        org_name = ""

    if org_name:
        await enrich_organization_info_from_name(row, tool_config=tool_config)
    return row


async def check_for_required_fields_company(file_input: str, file_output: str) -> None:
    """
    Reads rows from file_input and writes only rows that have both
    'company_linkedin_url' and 'primary_domain_of_organization' to file_output,
    ensuring no duplicates.
    """
    valid_rows = []
    seen_linkedin_urls = set()
    seen_primary_domains = set()

    with open(file_input, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            linkedin_url = row.get("company_linkedin_url", "").strip()
            primary_domain = row.get("primary_domain_of_organization", "").strip()

            if linkedin_url and primary_domain:
                if linkedin_url not in seen_linkedin_urls and primary_domain not in seen_primary_domains:
                    valid_rows.append(row)
                    seen_linkedin_urls.add(linkedin_url)
                    seen_primary_domains.add(primary_domain)

    # Write filtered rows to output
    with open(file_output, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(valid_rows)


async def find_and_add_lead_linkedin_url(file_input: str, file_output: str) -> None:
    """
    Reads rows from file_input. If user_linkedin_url is missing, attempts to find it using
    the Google Custom Search by job title, location, and organization name.
    Writes only rows that end up with a non-empty user_linkedin_url to file_output.
    """
    valid_rows = []
    with open(file_input, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            org_name = row.get("organization_name", "").strip()
            user_linkedin_url = row.get("user_linkedin_url", "").strip()
            if not user_linkedin_url:
                name = row.get("first_name", "").strip() + ' ' + row.get("last_name", "").strip()
                title = row.get("title", "CXO")
                location = row.get("location", "US")
                user_linkedin_url = await find_user_linkedin_url_google(user_name=name, user_title=title, user_location=location, user_company=org_name)
                row["user_linkedin_url"] = user_linkedin_url

            if user_linkedin_url:
                valid_rows.append(row)

    # Ensure the final CSV has the new "user_linkedin_url" column
    fieldnames = reader.fieldnames
    if "user_linkedin_url" not in fieldnames:
        fieldnames.append("user_linkedin_url")

    with open(file_output, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(valid_rows)


@assistant_tool
async def enrich_sales_navigator_leads(input_leads_file: List[str], enriched_leads_file: str) -> None:
    """
    High-level function that:
      1. Reads in multiple CSV files from input_leads_file
      2. Enriches each row's organization info
      3. (Optionally) Enriches each row's user LinkedIn URL (placeholder below)
      4. Writes all enriched data to a single CSV file enriched_leads_file
    """
    all_rows = []
    fieldnames = set()
    seen_lead_salesnav_urls = set()
    seen_linkedin_urls = set()

    # Read from each file and enrich
    for single_file in input_leads_file:
        print(f"Processing file: {single_file}...")
        with open(single_file, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                lead_salesnav_url = row.get("lead_salesnav_url", "").strip()
                if not lead_salesnav_url or lead_salesnav_url in seen_lead_salesnav_urls:
                    continue
                seen_lead_salesnav_urls.add(lead_salesnav_url)

                # Enrich the organization/company information
                await enrich_organization_information(row)
                user_linkedin_url = row.get("user_linkedin_url", "").strip()
                if not user_linkedin_url:
                    name = row.get("first_name", "").strip() + ' ' + row.get("last_name", "").strip()
                    title = row.get("title", "CXO")
                    location = row.get("location", "US")
                    org_name = row.get("organization_name", "").strip()
                    user_linkedin_url = await find_user_linkedin_url_google(user_name=name, user_title=title, user_location=location, user_company=org_name)
                    row["user_linkedin_url"] = user_linkedin_url

                if user_linkedin_url and user_linkedin_url not in seen_linkedin_urls:
                    seen_linkedin_urls.add(user_linkedin_url)
                    all_rows.append(row)
                    fieldnames.update(row.keys())

    # Define the order of the columns
    ordered_fieldnames = ["name", "title", "organization_name", "user_linkedin_url", "company_linkedin_url"]
    remaining_fieldnames = [field for field in fieldnames if field not in ordered_fieldnames]
    final_fieldnames = ordered_fieldnames + remaining_fieldnames

    # Write all enriched rows to the final output file
    if not all_rows:
        print("No data to write.")
        return

    with open(enriched_leads_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=final_fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"Enriched data written to: {enriched_leads_file}")
    return enriched_leads_file


