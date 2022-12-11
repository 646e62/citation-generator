'''
CanLII API calls
'''
import re
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
    # Check to see if the URL is a short URL
    # Short CanLII URLs use the .ca domain
    # Full CanLII URLs use the .org domain
    if "canlii.ca" in url:
        return "Short URL detected. Please use the long URL."
    # Removes query terms from the URL, if any
    if "?" in url:
        url = url.split('?')[0]
    url = url.split('/')
    case_id: str = url[-2]
    database_id: str = url[-5]
    language: str = url[-7]
    # Checks to see if the string starts with four numbers
    # Returns the caseID if it does
    if not re.match(r"^\d{4}", case_id):
        return "Invalid URL."
    # Properly formats SCC database IDs
    if database_id == "scc":
        database_id = "csc-scc"
    # Returns the caseID, databaseID, and language
    return language, database_id, case_id

def call_api(url: str) -> str:
    '''
    Calls the CanLII API and returns the JSON file.
    '''
    api_key: str = get_api_key()
    api_elements = case_info(url)
    language = api_elements[0]
    database_id = api_elements[1]
    case_id = api_elements[2]
    # CanLII API URL
    url: str = "https://api.canlii.org/v1/caseBrowse/" + language + "/" + \
        database_id + "/" + case_id + "/?api_key=" + api_key
    # Downloads the JSON file
    response = requests.get(url, timeout=50)
    # Converts the JSON file to a Python dictionary
    data = json.loads(response.text)
    # Returns the JSON file
    return data
    