from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import Http404
from django.http import HttpResponse
from django.contrib import messages

from .models import Changelog, Citation, Submission
from .scripts.mcgill_jurisprudence_rules import generate_citation, generate_pinpoint, sort_citations
from .scripts.api_calls import call_api_jurisprudence
from .scripts.database_functions import save_citation
from datetime import datetime

def index(request):
    return render(request, 'app/index.html')


def changelog(request):
    changelog = Changelog.objects.all()
    return render(request, 'app/changelog.html', {'changelog': changelog})


def process_text(request):
    # Get the text
    if request.method == 'POST':
        url = request.POST['url']
        pinpoint_number = request.POST['pinpoint']
        pinpoint_type = request.POST['pinpoint_type']
        parallel_citations = request.POST['parallel_citations']
        pinpoint_result = generate_pinpoint(pinpoint_number, pinpoint_type)

        # Check to see if the result is already in the database
        try:
            citation_model = Citation.objects.get(url=url)
            citation_data = model_to_dict(citation_model)
            sorted_citations = sort_citations(citation_data, parallel_citations)
            result = generate_citation(citation_data, sorted_citations, pinpoint_result)
            get_user_info(request)
            return render(request, 'app/result.html', {'result': result[1], 'sorted_citations': sorted_citations})

        # Call the API if it is not
        except Citation.DoesNotExist:
            citation_data = call_api_jurisprudence(url)
            if citation_data is None:
                messages.error(request, "Cannot get citation data")
                return render(request, 'app/index.html')
            else:
                # Save the citation data to the database
                sorted_citations = sort_citations(citation_data, parallel_citations)
                result = generate_citation(citation_data, sorted_citations, pinpoint_result)
                citation = save_citation(citation_data, url, result[0])
                get_user_info(request)
                return render(request, 'app/result.html', {'result': result[1], 'sorted_citations': sorted_citations})

    else:
        return render(request, 'app/index.html')


def get_user_info(request):
    '''
    This function gets and stores information about the user's request using
    the Submissions class in models.py
    '''
    url = request.POST['url']
    ip_address = request.META['REMOTE_ADDR']
    date = datetime.now()

    submission = Submission(url=url, ip_address=ip_address, date=date)
    submission.save()

