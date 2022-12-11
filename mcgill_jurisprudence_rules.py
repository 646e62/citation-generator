'''
Rules.

TODO:
- Function: Define a function to handle bulk printed reporter citations
  - Rule: add the correct year to print citations where needed
  - Rule: remove excess punctuation from print citations
'''

from api_calls import call_api

from data.mcgill.appendices import b3_neutral_citations_en

neutral_citations = []
for item in b3_neutral_citations_en[:, 2]:
    neutral_citations.append(item)

def enter_pinpoint() -> str:
    '''
    Asks the user to enter a pinpoint. The function returns the pinpoint.
    '''
    # Verifies that the user has inputted a number for the pinpoint
    try:
        pinpoint = int(input("Enter the pinpoint: "))
        return pinpoint
    except ValueError:
        return "Invalid pinpoint."

def verify_neutral_citation(citation: str, neutral_citation_list: list) -> bool:
    '''
    Checks to see if the citation is neutral. Neutral citations are always
    preferred and obviate the need for a printed reporter citation. If the
    citation is neutral, the function returns True. If not, it returns False.
    '''
    #parsed_citation = citation.split(" ")
    court_level = citation[1]
    for unclassified_citation in neutral_citation_list:
        if court_level in unclassified_citation:
            return True
    return False

def generate_case_citation(url: str) -> str:
    '''
    Generates a citation from the JSON file. This currently only works for
    cases that use neutral citations. Citations using printed reporters will
    be added in the near future.
    '''
    # Calls the CanLII API
    data = call_api(url)

    # Extracts the style of cause and removes all periods
    style_of_cause = data["title"].replace(".", "")
    # Verifies that the citation is neutral
    parsed_citation = data["citation"].split(" ")

    if verify_neutral_citation(parsed_citation, neutral_citations) is True:
        neutral_citation_list = data["citation"].split()
        neutral_citation = " ".join(neutral_citation_list[:3])
        # Adds the SCR printed citation whenever it's available
        # This accords with the official reporter hierarchy in McGill 9e 3.1
        if "SCR" in parsed_citation:
            pinpoint = enter_pinpoint()
            official_reporter = " ".join(neutral_citation_list[-4:-1])
            citation = f"*{style_of_cause}*, {neutral_citation}, "\
                       f"{official_reporter} at para {pinpoint}."
        else:
            pinpoint = enter_pinpoint()
            citation = f"*{style_of_cause}*, {neutral_citation} at para "\
                       f"{pinpoint}."
        return citation
    else:
        generate_print_reporter_citations()

def generate_print_reporter_citations() -> str:
    '''
    Generates a printed reporter citation.
    '''
    printed_reporter_string = "[2017] SCJ No 60 (QL) — EYB 2017-287963 — "\
        "142 WCB (2d) 343 — 396 CRR (2d) 212 — 357 CCC (3d) 350 — "\
        "42 CR (7th) 74 — [2017] EXP 3391 — 418 DLR (4th) 382"
    if " — " in printed_reporter_string:
        print(printed_reporter_string.split(" — "))
    else:
        print(printed_reporter_string.split(", "))

    return "Neutral citation not found."
