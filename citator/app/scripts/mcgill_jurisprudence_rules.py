'''
This module generates McGill 9e Jurisprudence citations.
'''
import sys
import re

from django.utils.safestring import SafeString
from .data.mcgill import reporter_data
from .cache import serialize

# Functions for the McGill 9e Jurisprudence class

# Determines whether the string contains a neutral citation

def check_neutral_citation(neutral_citation: str) -> bool:
    '''
    Checks to see if the citation is neutral. Neutral citations are always
    preferred and obviate the need for a printed reporter citation. If the
    citation is neutral, the function returns True. If not, it returns False.
    '''
    # Change to use the any() function
    neutral_citation_list = [item[2] for item in reporter_data.neutral_citations_ca]
    court_level = neutral_citation.split()[1]
    for unclassified_citation in neutral_citation_list:
        if court_level in unclassified_citation:
            return True
    return False

# Takes a string of citations copied directly from CanLII, cleans the data,
# and returns a list of parallel citations

def process_parallel_citations(other_citations: str) -> tuple[str, str]:
    '''
    The function returns a list of parallel citations inferred from a block
    of text copied and pasted by the user.

    When copied from CanLII, the function returns a list of (presumably
    correct) parallel citations. The citations are separated by a long dash
    (—) and are preceded by a space. The function splits the block of text
    into a list of citations and removes the preceding space. The function
    then removes any citation elements that are in the exclude list. So
    far, this only includes the QuickLaw designation (QL). The function
    must make a small adjustment to the year of the citation if Westlaw
    reported the case.

    For citations copied directly from Westlaw, the function will likely
    only need to remove superfluous periods, after which point the
    citations will likely be correct. This functionality will be added in
    the near future.

    The function presently doesn't distinguish between the various
    items inside the string (e.g. the reporter, the year, the volume,
    etc.). This will be added in the near future.
    '''

    # Creates (likely incomplete) sets of citation and reporter elements to
    # exclude
    excluded_citations = ("(QL)")
    excluded_reporters = ("No", "no")

    # Creates a list of parallel citations if the user copied the citations
    # from CanLII. Assumes that the citations are separated by a long dash
    # (—) and preceded by a space. Assumes perfect input.

    # Separates the parallel citations, if any, into a list
    if other_citations and "—" not in other_citations:
        citation_list = [other_citations]
    elif not other_citations:
        citation_list = []
    else:
        citation_list = other_citations.split("—")
        citation_list = [item.strip() for item in citation_list]

    citation_list_parsed = []
    parallel_reporter_list = []

    # Parses the list of parallel citations
    # Some reporters have names that are separated by a space (eg "Sask R")
    # This function will need to be updated to handle these cases

    for case in citation_list:
        # Splits the citation into a list
        # Splits either by space or by dash
        #print(case)
        delimiters = " |-"
        citation_split = re.split(delimiters, case)

        # Light formatting
        for item in citation_split:
            # Remove items that are in the exclude list
            if item in excluded_citations:
                citation_split.remove(item)
                case = " ".join(citation_split)
            # Adds the parallel reporter
            if item.isalpha() and item not in excluded_reporters:
                # Remove the periods from the reporter
                item = item.replace(".", "")
                parallel_reporter_list.append(item)

            # Remove brackets around a number if the next item is a string containing "Carswell"
            # See McGill 9e 3.8.3
            if item.startswith("[") and \
                item.endswith("]") and \
                citation_split[citation_split.index(item) + 1].startswith("Carswell"):
                citation_split[citation_split.index(item)] = item[1:-1]
                case = " ".join(citation_split)

        # Join the parallel_reporter_list back into a string
        # This is necessary because the list is used to create a set

        parallel_reporter_list = " ".join(parallel_reporter_list)
        print(parallel_reporter_list)        
        citation_list_parsed.append(case)

    return parallel_reporter_list


# Adds/removes years, jurisdictions, and court levels to/from citations

def verify_year(citation: str, citation_data: dict) -> str:
    '''
    Some citations require a year to be added to the citation. This function
    adds the year to the citation if necessary. 

    The following rules apply to adding years to citations:

    1. When a decision has a neutral citation or when the decision year is the
    same as the year in the main citation, the year isn't added to the style
    of cause and the citation remains the same.

    2. When the main citation doesn't contain a year, one is added in 
    parentheses after the sytle of cause.

    3. If the main citation's year is different from the decisions year, the
    decision year is provided in parentheses after the style of cause.


    Therefore, the first step this function should take is to check
    to see whether the citation is the main citation, and if so, whether the
    citation contains a year. If the citation is the main citation and it
    contains a year, the function checks to see whether the year in the
    citation matches the year of the decision.
    
    This function should not be called when the program has already detected
    a neutral citation, or when the citation is a parallel citation.
    '''

    # Creates a list of citation elements
    citation_list = citation.split()
    if citation_data["decisionDate"]:
        decision_year = citation_data["decisionDate"].split("-")[0]
    else:
        decision_year = citation_data["date"][0]
    style_of_cause = citation_data["title"].replace(".", "") 
    reporter_year = None

    # Check to see if the first element of the citation is a year. Note that 
    # many citations are enclosed in square brackets that will need to be 
    # stripped to compare to the decision year. Where a citation contains a 
    # year, it is (almost always) the first element of the citation.

    check_brackets = re.search(r"\[\d{4}\]", citation_list[0])
    check_year = re.search(r"\b\d{4}\b", citation_list[0])

    if check_brackets:
        reporter_year = "".join(char for char in citation_list[0] if char.isdigit())
    if check_year:
        reporter_year = citation_list[0]

    if reporter_year == decision_year:
        citation_year_corresponds = True
    else:
        citation_year_corresponds = False

    # When a decision has a neutral citation or when the decision year is the
    # same as the year in the main citation, the year isn't added to the style
    # of cause and the citation remains the same.
        
    if citation_year_corresponds:
        return citation, style_of_cause

    # When the main citation doesn't contain a year, or if the main citation's
    # year is different from the decisions year, the decision year is provided
    # in parentheses after the style of cause.

    elif not reporter_year or reporter_year != decision_year:
        citation = f"{style_of_cause} ({decision_year})"
        return citation, style_of_cause
    


# Sorts parallel citations into one of five categories: neutral, official,
# preferred, authoritative, and unofficial

def sort_citations(citation_data: dict, user_citations: str) -> dict:
    '''
    This function takes a list of citations and sorts them into official,
    preferred, authoritative, and unofficial citations. It returns a dictionary
    containing the sorted citations.
    '''
    
    citation_list = process_parallel_citations(user_citations)
    
    neutral_citations = []
    official_reporters = []
    preferred_reporters = []
    authoritative_reporters = []
    unofficial_reporters = []
    canlii_citation = citation_data["citation"]
    canlii_citation_list = canlii_citation.split()

    official_reporters_list = [reporter[0] for reporter in reporter_data.official_reporters]
    preferred_reporters_list = [reporter[0] for reporter in reporter_data.preferred_reporters]
    authoritative_reporters_list = [reporter[0] for reporter in reporter_data.authoritative_reporters]

    
    # Checks for an official reportercitation in the CanLII citation. If there 
    # is one, it is added to the citation list. The CanlII citation is then
    # added to the unofficial reporters list.
    if "SCR" in canlii_citation:
        official_reporter_citation = " ".join(canlii_citation_list[-4:])
        formatted_canlii_citation = " ".join(canlii_citation_list[:-4])
        official_reporters.append(official_reporter_citation)
        unofficial_reporters.append(formatted_canlii_citation)
    else:
        unofficial_reporters.append(canlii_citation)
    
    # Checks to see if the citation is a neutral citation
    if check_neutral_citation(canlii_citation) is True:
        # Generates the neutral citation
        neutral_citation = " ".join(canlii_citation_list[:3])
        neutral_citations.append(neutral_citation)

    # Cycle through citation_list if it is not empty
    if citation_list == []:
        return {"neutral": neutral_citations,\
                "official": official_reporters,\
                "preferred": preferred_reporters,\
                "authoritative": authoritative_reporters,\
                "unofficial": unofficial_reporters}
    else:
        reporters = citation_list[1]
        citations = citation_list[0]
        for citation in citation_list[1]:
            # Check to see if the reporter appears in a given list of reporters
            # If it does, the citation is added to the appropriate list
            #print(reporter_data.official_reporters)
            if citation in official_reporters_list:
                citation_index = citation_list[1].index(citation)
                official_reporters.append(citation_list[0][citation_index])
            elif citation in preferred_reporters_list:
                citation_index = citation_list[1].index(citation)
                preferred_reporters.append(citation_list[0][citation_index])
            elif citation in authoritative_reporters_list:
                citation_index = citation_list[1].index(citation)
                authoritative_reporters.append(citation_list[0][citation_index])
            else:
                citation_index = citation_list[1].index(citation)
                unofficial_reporters.append(citation_list[0][citation_index])
    #for citation in citation_list:
        #print(citation)
    
    return {"neutral": neutral_citations,\
        "official": official_reporters,\
        "preferred": preferred_reporters,\
        "authoritative": authoritative_reporters,\
        "unofficial": unofficial_reporters}


# Pinpoint handlers

def generate_pinpoint(pinpoint_number, pinpoint_type) -> str:
    '''
    Generates a pinpoint. The function returns the pinpoint.
    '''
    if pinpoint_type == "none":
        return ""
    elif pinpoint_type == "page":
        return f" at {pinpoint_number}"
    elif pinpoint_type == "para":
        return f" at para {pinpoint_number}"


def enter_pinpoint() -> str:
    '''
    Asks the user to enter a pinpoint. The function returns the pinpoint.
    '''
    try:
        pinpoint = int(input("Enter the pinpoint: "))
        return pinpoint
    except ValueError:
        return "Invalid pinpoint."


# Citation generator

def generate_citation(citation_data: dict, sorted_citations: dict, 
                      pinpoint_result: int | None = None) -> str:
    '''
    Generates a citation using the sorted citations dictionary. The citations
    are subject to the following hierarchy: neutral, official, preferred,
    authoritative, unofficial. The function returns the citation.
    '''

    if sorted_citations["neutral"]: 
        neutral_citation = sorted_citations["neutral"][0]
        style_of_cause = citation_data["title"].replace(".", "")
        if sorted_citations["official"]:
            official_reporter_citation = sorted_citations.get("official")[0]
            citation = SafeString(f"<em>{style_of_cause}</em>, {neutral_citation}, {official_reporter_citation}")
            pinpoint_citation = SafeString(f"<em>{style_of_cause}</em>, {neutral_citation}{pinpoint_result}, {official_reporter_citation}.")
        else:
            citation = SafeString(f"<em>{style_of_cause}</em>, {neutral_citation}")
            pinpoint_citation = SafeString(f"<em>{style_of_cause}</em>, {neutral_citation}{pinpoint_result}.")

        return citation, pinpoint_citation

    elif sorted_citations["official"]:
        official_reporter_citation = sorted_citations.get("official")[0]
        style_of_cause = verify_year(official_reporter_citation, citation_data)
        
        citation = SafeString(f"<em>{style_of_cause}</em>, {official_reporter_citation}")
        pinpoint_citation = SafeString(f"<em>{style_of_cause}</em>, {official_reporter_citation}{pinpoint_result}.")

        return citation, pinpoint_citation

    elif sorted_citations["preferred"]:
        preferred_reporter_citation = sorted_citations.get("preferred")[0]
        style_of_cause = verify_year(preferred_reporter_citation, citation_data)

        citation = SafeString(f"<em>{style_of_cause}</em>, {preferred_reporter_citation}")
        pinpoint_citation = SafeString(f"<em>{style_of_cause}</em>, {preferred_reporter_citation}{pinpoint_result}.")

        return citation, pinpoint_citation
    
    elif sorted_citations["authoritative"]:
        authoritative_reporter_citation = sorted_citations.get("authoritative")[0]
        style_of_cause = verify_year(authoritative_reporter_citation, citation_data)

        citation = SafeString(f"<em>{style_of_cause}</em>, {authoritative_reporter_citation}")
        pinpoint_citation = SafeString(f"<em>{style_of_cause}</em>, {authoritative_reporter_citation}{pinpoint_result}.")

        return citation, pinpoint_citation

    else:
        unofficial_reporter_citation = sorted_citations.get("unofficial")[0]
        style_of_cause = verify_year(unofficial_reporter_citation, citation_data)

        citation = SafeString(f"<em>{style_of_cause}</em>, {unofficial_reporter_citation}")
        pinpoint_citation = SafeString(f"<em>{style_of_cause}</em>, {unofficial_reporter_citation}{pinpoint_result}.")

        return citation, pinpoint_citation


# Basic CLI tool

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Call script with url")

    URL = sys.argv[1]
    ret = generate_citation(URL)
    print(ret)

