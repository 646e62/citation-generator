from ..models import Citation

def save_citation(citation_data, url, result):
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
    citation.databaseId = citation_data["databaseId"]
    citation.case_jurisdiction = url_split[4]
    citation.court = url_split[5]
    citation.caseId = citation_data["caseId"]
    citation.citation = citation_data["citation"]
    citation.decisionDate = citation_data["decisionDate"]
    citation.title = citation_data["title"]
    citation.docketNumber = citation_data["docketNumber"]
    citation.keywords = citation_data["keywords"].split(" — ")
    citation.mcgill_citation = result

    # Save the citation to the database.
    citation.save()

    # Return the citation object.
    return citation


