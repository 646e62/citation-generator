'''
CanLII API calls
'''
import json
# import datetime
# import numpy as np
import requests

def get_api_key() -> str:
    '''
    Retrieves the CanLII API key from the file system.
    '''
    canlii_api_key: str = "data/api/CANLII_API_KEY"
    try:
        with open(canlii_api_key, 'r', encoding="utf-8") as file:
            api_key: str = file.read()
        return api_key
    except FileNotFoundError:
        print(f"{canlii_api_key} not found")
        return None

def case_info(url: str) -> str:
    '''
    Verifies that the URL is a valid CanLII URL. Because CanLII throws a
    CAPTCHA when resolving short URLs, this function verifies that the URL is a
    long URL. Because the function works by parsing the CanLII URL's
    predictable structure, it also checks to see whether the user inputted the
    scheme (https) and subdomain (www). If so, they're removed. If CanLII
    changes their URL structure, this function will need to be updated.
    '''
    # Check to see if the URL is a short URL. Short CanLII URLs use the .ca
    # domain, while full CanLII URLs use the .org domain
    CANLII_SHORT = "canlii.ca"
    CANLII_LONG = "canlii.org"
    if CANLII_SHORT in url:
        print("Short URL detected. Please use the long URL.")
        return None
    if CANLII_LONG not in url:
        print("Invalid URL.")
        return None
    
    # Removes query terms from the URL, if any
    if "?" in url:
        url = url.split('?')[0]
    if "/" not in url:
        return None
    url = url.split('/')

    # If the URL list contains less than 8 items, it's not a valid CanLII URL
    if len(url) < 8:
        return None
    case_id: str = url[-2]
    database_id: str = url[-5]
    language: str = url[-7]
    if database_id == "scc":
        database_id = "csc-scc"

    # Rudimentary error checking
    # Verifies whether case_id begins with four digits
    # Future versions should check to see whether the middle case_id component
    # follows the correct format (ie, jurisdiction-court/reporter string
    # followed by an identifying number)
    if case_id[:4].isdigit():
        # Returns the caseID, databaseID, and language
        return language, database_id, case_id
    else:
        print("Invalid URL")
        return None

def call_api_jurisprudence(url: str) -> str:
    '''
    Calls the CanLII API and returns the JSON file.
    '''
    api_key: str = get_api_key()
    api_elements = case_info(url)

    if api_elements is None:
        return None
    language, database_id, case_id = api_elements
    
    # CanLII API URL
    url: str = "https://api.canlii.org/v1/caseBrowse/" + language + "/" + \
        database_id + "/" + case_id + "/?api_key=" + api_key
    # Downloads the JSON file
    response = requests.get(url, timeout=50)
    # Converts the JSON file to a Python dictionary
    data = response.json()
    # Returns the JSON file
    return data
    