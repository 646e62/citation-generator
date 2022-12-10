'''
CanLII API calls
'''

def get_api_key():
    '''
    Retrieves the CanLII API key from the file system.    
    '''
    canlii_api_key = "../data/api/CANLII_API_KEY"
    try:
        with open(canlii_api_key, 'r', encoding="utf-8") as file:
            api_key = file.read()
        return api_key
    except FileNotFoundError:
        print(f"{canlii_api_key} not found")
        return None
