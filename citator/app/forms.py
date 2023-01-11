from django import forms

class MyForm(forms.Form):
    CHOICES = (
        ('option_1', 'Option 1'),
        ('option_2', 'Option 2'),
    )
    radio_field = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

class PinpointType(forms.Form):
    '''
    Defines the form for the type of pinpoint, if any.
    In the near future, the code will be modified to allow the user to
    select what kind of pinpoint citation they wish to add, if any. The output
    will vary depending on what the user selects.

    The code will eventually have to account for citations referencing multiple
    pages or paragraphs, including ranges and multiple individual pinpoints for
    a single citation. 

    Eg: *R v AH*, 2022 SKPC 46 at paras 4 — 6, 12 & 15.

    Future versions will also need to include additional pinpoint types, such 
    as sections and articles (for legislation), numbers for journals, and 
    footnotes for all types of documents. See McGill 9e 1.5 for more details.
    '''
    CHOICES = (
        ('paragraph', 'Paragraph'),
        ('page', 'Page'),
        ('none', 'None'),
    )

class CaseJurisdiction(forms.Form):
    CHOICES = (
        ('ca', 'Canada'),
        ('bc', 'British Columbia'),
        ('ab', 'Alberta'),
        ('sk', 'Saskatchewan'),
        ('mb', 'Manitoba'),
        ('on', 'Ontario'),
        ('qc', 'Quebec'),
        ('nb', 'New Brunswick'),
        ('ns', 'Nova Scotia'),
        ('pe', 'Prince Edward Island'),
        ('nl', 'Newfoundland and Labrador'),
        ('nt', 'Northwest Territories'),
        ('yt', 'Yukon'),
        ('nu', 'Nunavut'),
    )
    
    jurisdiction = forms.ChoiceField(choices=CHOICES)
