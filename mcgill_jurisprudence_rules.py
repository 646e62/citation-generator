'''
This module generates McGill 9e Jurisprudence citations.gener
'''
import sys

from api_calls import call_api_jurisprudence
import data.mcgill.reporter_data as reporter_data

# Functions for the McGill 9e Jurisprudence class

def verify_neutral_citation(neutral_citation: str,
                            neutral_citation_list: list) -> bool:
    '''
    Checks to see if the citation is neutral. Neutral citations are always
    preferred and obviate the need for a printed reporter citation. If the
    citation is neutral, the function returns True. If not, it returns False.
    '''
    # Change to use the any() function
    court_level = neutral_citation[1]
    for unclassified_citation in neutral_citation_list:
        if court_level in unclassified_citation:
            return True
    return False

def isolate_parallel_citations(other_citations: str) -> str:
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

    # Creates lists of citation and reporter elements to exclude
    # These lists are (very likely) incomplete
    citation_exclude_list = ["(QL)"]
    reporter_exclude_list = ["No"]

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
            if item in citation_exclude_list:
                citation_split.remove(item)
                case = " ".join(citation_split)
            # Adds the parallel reporter
            if item.isalpha() and item not in reporter_exclude_list:
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

def check_preferred_reporters(parallel_reporters: list): # -> str:
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
        print(reporter)
        # Add official reporter functionality
        for item in reporter_data.preferred_reporters:
            if reporter == item[0]:
                preferred_reporters.append(reporter)
        for item in reporter_data.authoritative_reporters:
            if reporter == item[0]:
                authoritative_reporters.append(reporter)
        else:
            unofficial_reporters.append(reporter)
    return f"Preferred reporters: {preferred_reporters}",\
            f"Authoritative reporters: {authoritative_reporters}",\
            f"Unofficial reporters: {unofficial_reporters}"


def enter_pinpoint() -> str:
    '''
    Asks the user to enter a pinpoint. The function returns the pinpoint.
    '''
    try:
        pinpoint = int(input("Enter the pinpoint: "))
        return pinpoint
    except ValueError:
        return "Invalid pinpoint."


def generate_citation(url) -> str:
    '''
    Generates a citation from the JSON file. This currently only works for
    cases that use neutral citations. Citations using printed reporters will
    be added in the near future.
    '''
    # Calls the CanLII API
    data = call_api_jurisprudence(url)
    if data is None:
        return "Invalid URL."

    # Creates a list of neutral citations from the McGill 9e Appendix B3
    # stored in data/mcgill/appendices.py
    neutral_citations = []
    for item in reporter_data.neutral_citations_ca:
        neutral_citations.append(item[2])

    # Extracts the style of cause and removes all periods
    style_of_cause = data["title"].replace(".", "")
    # Verifies that the citation is neutral
    parsed_citation = data["citation"].split(" ")

    if verify_neutral_citation(parsed_citation, neutral_citations) is True:
        neutral_citation_list = data["citation"].split()
        neutral_citation = " ".join(neutral_citation_list[:3])
        pinpoint = enter_pinpoint()

        # Adds the SCR printed citation whenever it's available
        # This accords with the official reporter hierarchy in McGill 9e 3.1
        # The SCR abbreviation is unique, as it is always included in CanLII
        # citations when the citation is available. It is also good practice
        # to include the SCR citation whenever possible, as it is for an
        # official reporter.
        if "SCR" in parsed_citation:
            official_reporter_citation = " ".join(neutral_citation_list[-4:])
            citation = f"*{style_of_cause}*, {neutral_citation} at "\
                f"para {pinpoint}, {official_reporter_citation}."
        else:
            citation = f"*{style_of_cause}*, {neutral_citation} at para "\
                    f"{pinpoint}."
        return citation
    else:
        parallel_citation_string = input("Enter the unofficial reporters"\
            "by copying them directly from a CanLII case or separating"\
            "them with commas: ")

        parallel_citations, parallel_reporters = \
            isolate_parallel_citations(parallel_citation_string)

        # Move everything into the function and remove the following code
        # *****
        preferred_reporters = []
        authoritative_reporters = []
        unofficial_reporters = []

        # Categorizes the parallel reporters as preferred, authoritative,
        # or unofficial

        for reporter in parallel_reporters:
            print(reporter)
            for item in reporter_data.preferred_reporters:
                if reporter == item[0]:
                    preferred_reporters.append(reporter)
            for item in reporter_data.authoritative_reporters:
                if reporter == item[0]:
                    authoritative_reporters.append(reporter)
            else:
                unofficial_reporters.append(reporter)
        return f"Preferred reporters: {preferred_reporters}",\
               f"Authoritative reporters: {authoritative_reporters}",\
               f"Unofficial reporters: {unofficial_reporters}"
        # *****


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Call script with url")

    url = sys.argv[1]
    ret = generate_citation(url)
    print(ret)
