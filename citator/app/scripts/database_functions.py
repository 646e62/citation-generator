from ..models import Citation

def save_citation(citation_data, url):
    '''
    Save the data from the API call to the Django database.
    '''
    
    # Create a new citation object.
    citation = Citation()
    url_split = url.split("/")

    # Set the citation's attributes.
    citation.url = url
    citation.short_url = citation_data["url"]
    citation.language = citation_data["language"]
    citation.database_id = citation_data["databaseId"]
    citation.case_jurisdiction = url_split[4]
    citation.court = url_split[5]
    citation.case_id = citation_data["caseId"]
    citation.canlii_citation = citation_data["citation"]
    citation.date = citation_data["decisionDate"]
    citation.style_of_cause = citation_data["title"]
    citation.docket_number = citation_data["docketNumber"]
    citation.keywords = citation_data["keywords"].split(" — ")

    # Save the citation to the database.
    citation.save()

    # Return the citation object.
    return citation


