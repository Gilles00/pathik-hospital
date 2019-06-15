import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from mainapp.forms import RegForm
from mainapp.models import Patient


def index(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegForm()

    return render(request, 'mainapp/index.html', {'form': form})


def view_patient(request, patient_id):
    print(patient_id)
    patient = Patient.objects.get(id=patient_id)
    current_date = datetime.datetime.now().date()

    days_left = current_date - patient.dob

    years = ((days_left.total_seconds()) / (365.242 * 24 * 3600))
    years_int = int(years)

    months = (years - years_int) * 12
    months_int = int(months)

    days = (months - months_int) * (365.242 / 12)
    days_int = int(days)

    context = {
        'patient': patient,
        'age': "{} years, {} months, {} days".format(years_int, months_int, days_int),
    }
    return render(request, 'mainapp/view_patients.html', context)
