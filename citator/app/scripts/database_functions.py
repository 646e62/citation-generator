def save_citation(citation_data, url):
    '''
    Save the data from the API call to the Django database.
    '''
    
    # Create a new citation object.
    citation = Citation()

    # Set the citation's attributes.
    citation.url = url
    citation.short_url = citation_data['url']

    citation.url = citation_data['citation_number']
    citation.citation_date = citation_data['citation_date']
    citation.citation_time = citation_data['citation_time']
    citation.citation_location = citation_data['citation_location']
    citation.citation_violation = citation_data['citation_violation']
    citation.citation_amount = citation_data['citation_amount']
    citation.citation_status = citation_data['citation_status']
    citation.citation_officer = citation_data['citation_officer']
    citation.citation_agency = citation_data['citation_agency']

    # Save the citation to the database.
    citation.save()

    # Return the citation object.
    return citation


