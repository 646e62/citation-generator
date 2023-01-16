'''
This module generates McGill 9e Jurisprudence citations.gener
'''
import sys

from django.utils.safestring import SafeString
from .data.mcgill import reporter_data as reporter_data
from .cache import serialize

# Functions for the McGill 9e Jurisprudence class

def verify_neutral_citation(neutral_citation: str,
                            neutral_citation_list: list) -> bool:
    '''
    Checks to see if the citation is neutral. Neutral citations are always
    preferred and obviate the need for a printed reporter citation. If the
    citation is neutral, the function returns True. If not, it returns False.
    '''
    # Change to use the any() function
    print(neutral_citation)
    court_level = neutral_citation.split(" ")[1]
    for unclassified_citation in neutral_citation_list:
        if court_level in unclassified_citation:
            return True
    return False

def isolate_parallel_citations(other_citations: str) -> tuple[str, str]:
    '''
    The function returns a list of parallel citations inferred from a block
    of text copied and pasted by the user.

    When copied from CanLII, the function returns a list of (apparently
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

    # Creates (likely incomplete sets of citation and reporter elements to
    # exclude
    excluded_citations = ("(QL)")
    excluded_reporters = ("No")

    # Creates a list of parallel citations if the user copied the citations
    # from CanLII
    if "—" in other_citations:
        citation_list = other_citations.split("—")
        citation_list = [item.strip() for item in citation_list]

    citation_list_parsed = []
    parallel_reporter_list = []

    # Parses the list of parallel citations
    for case in citation_list:
        # Splits the citation into a list
        citation_split = case.split(" ")

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

        citation_list_parsed.append(case)

    return citation_list_parsed, parallel_reporter_list

def check_preferred_reporters(parallel_reporters: list,
                              parallel_citations: list,
                              scr_in_title: str): # -> str:
    '''
    Checks to see which of the parallel citations are preferred. The
    function evaluates each list item and determines whether the citation
    is official, preferred, authoritative, unofficial, or unlisted. The
    function reports on its findings, listing the citations in order of
    preference, if any. The function assumes that the program has already
    dealt with neutral citations.
    '''
    # Search preferred_reporters for the reporter abbreviations and see if
    # the abbreviation string exists in the preferred_reporters list
    official_reporters = []
    preferred_reporters = []
    authoritative_reporters = []
    unofficial_reporters = []

    # Categorizes the parallel reporters as preferred, authoritative,
    # or unofficial

    for reporter in parallel_reporters:
        '''
        Add official reporter functionality
        '''
        corresponding_citation = parallel_citations[
            parallel_reporters.index(reporter)]

        for item in reporter_data.official_reporters:
            if reporter in item:
                official_reporters.append(corresponding_citation)
                break
        for item in reporter_data.preferred_reporters:
            if reporter in item:
                preferred_reporters.append(corresponding_citation)
                break
        for item in reporter_data.authoritative_reporters:
            if reporter in item:
                authoritative_reporters.append(corresponding_citation)
                break

        if corresponding_citation not in preferred_reporters and \
            corresponding_citation not in authoritative_reporters and \
            corresponding_citation not in official_reporters:
            unofficial_reporters.append(corresponding_citation)

    return {"official": official_reporters,\
            "preferred": preferred_reporters,\
            "authoritative": authoritative_reporters,\
            "unofficial": unofficial_reporters}

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


def generate_citation(citation_data, pinpoint_result: int | None = None) -> str:
    '''
    Generates a citation from the JSON file. This currently only works for
    cases that use neutral citations. Citations using printed reporters will
    be added in the near future.
    '''
    # Creates a list of neutral citations from the McGill 9e Appendix B3
    # stored in data/mcgill/appendices.py
    neutral_citations = []
    for item in reporter_data.neutral_citations_ca:
        neutral_citations.append(item[2])

    
    print(citation_data)
    
    # Extracts the style of cause and removes all periods
    style_of_cause = citation_data["title"].replace(".", "") 
    parsed_citation = citation_data["citation"]


    if verify_neutral_citation(parsed_citation, neutral_citations) is True:
        neutral_citation_list = parsed_citation.split(" ")
        neutral_citation = " ".join(neutral_citation_list[:3])

        # Adds the SCR printed citation whenever it's available
        # This accords with the official reporter hierarchy in McGill 9e 3.1
        # The SCR abbreviation is unique, as it is always included in CanLII
        # citations when the citation is available. It is also good practice
        # to include the SCR citation whenever possible, as it is for an
        # official reporter.

        # Refactor to feed the SCR citation into the check_preferred_reporters
        # function

        if "SCR" in parsed_citation:
            official_reporter_citation = " ".join(neutral_citation_list[-4:])
        else:
            official_reporter_citation = None
        if official_reporter_citation:
            citation = SafeString(f"<em>{style_of_cause}</em>, {neutral_citation}, {official_reporter_citation}")
            pinpoint_citation = SafeString(f"<em>{style_of_cause}</em>, {neutral_citation}{pinpoint_result}, {official_reporter_citation}.")
        else:
            citation = SafeString(f"<em>{style_of_cause}</em>, {neutral_citation}")
            pinpoint_citation = SafeString(f"<em>{style_of_cause}</em>, {neutral_citation}{pinpoint_result}.")
        print(citation)
        return citation, pinpoint_citation

    else:
        return generate_parallel_citation(official_reporter_citation)

    # Define some rules for adding parallel citations to cases with and without
    # neutral citations

def generate_parallel_citation(scr_in_title: str) -> dict:
    '''
    Produces a list of parallel citations from a string when called.
    '''
    parallel_citation_string = input("Enter the unofficial reporters"\
            "by copying them directly from a CanLII case or separating"\
            "them with commas: ")

    parallel_citations, parallel_reporters = isolate_parallel_citations(
        parallel_citation_string)

    parallel_reporters = check_preferred_reporters(
        parallel_reporters, parallel_citations, scr_in_title)

    return parallel_reporters

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Call script with url")

    URL = sys.argv[1]
    ret = generate_citation(URL)
    print(ret)
