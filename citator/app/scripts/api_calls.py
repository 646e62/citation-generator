'''
CanLII API calls
'''
# import datetime
import requests
from decouple import config

# Short CanLII URLs use the .ca domain, while full CanLII URLs use the .org
# domain
CANLII_SHORT = "canlii.ca"
CANLII_LONG = "canlii.org"
REQ_CANLII_URL_COMPONENTS = 8

def get_database_id(database_id: str) -> str:
    '''
    Checks to see whether the URL's databaseID component is the same as the
    actual databaseID. If not, it returns the actual databaseID. Fixes a problem
    where hyphenated databaseIDs weren't being recognized.
    '''

    hyphenated_database_ids = [
        ["cbsc-ccnr", ["cbsc", "ccnr"]],
        ["citt-tcce", ["citt", "tcce"]],
        ["csc-scc-al", ["csc-a", "scc-l"]],
        ["cci-tcc", ["cci", "tcc"]],
        ["csc-scc", ["csc", "scc"]],
        ["casa-cala", ["casa", "cala"]],
        ["sst-tss", ["sst", "tss"]],
        ["cmac-cacm", ["cmac", "cacm"]],
        ["cart-crac", ["cart", "crac"]],
        ["pcc-cvpc", ["pcc", "cvpc"]],
        ["sct-trp", ["sct", "trp"]],
        ["cer-rec", ["cer", "rec"]],
        ["exchc-cech", ["exchc", "cech"]],
        ]
    
    # Run through the hyphenated databaseIDs and check to see whether the 
    # database_id component matches either of the second elements in the list. 
    # If so, return the first element in the list as the database_id

    for database in hyphenated_database_ids:
        if database_id in database[1]:
            return database[0]
    return database_id


def get_api_key() -> str:
    '''
    Retrieves the CanLII API key from the file system.
    '''
    return config('CANLII_API_KEY')

def case_info(url: str) -> str:
    '''
    Verifies that the URL is a valid CanLII URL. Because CanLII throws a
    CAPTCHA when resolving short URLs, this function verifies that the URL is a
    long URL. Because the function works by parsing the CanLII URL's
    predictable structure, it also checks to see whether the user inputted the
    scheme (https) and subdomain (www). If so, they're removed. If CanLII
    changes their URL structure, this function will need to be updated.
    '''

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

    if len(url) < REQ_CANLII_URL_COMPONENTS:
        return None
    case_id: str = url[-2]
    database_id: str = get_database_id(url[-5])
    language: str = url[-7]

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

    # CanLII API URL call structure
    url: str = f"https://api.canlii.org/v1/caseBrowse/{language}/"\
        f"{database_id}/{case_id}/?api_key={api_key}"
    response = requests.get(url, timeout=50)
    # Converts the JSON file to a Python dictionary
    data = response.json()
    return data
