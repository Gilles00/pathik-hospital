import datetime

from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render

from mainapp.forms import RegForm
from mainapp.models import Patient


def manage_patients(request):
    form: RegForm = RegForm()
    return render(request, 'mainapp/manage_patients.html', {'form': form})


def register_patient(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            patient = form.save()
            return redirect('viewPatient', patient.id)

    # if a GET (or any other method)
    else:
        return redirect('/')


def view_patient(request, patient_id):
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


def print_sticker(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    context = {
        'patient': patient,
    }
    return render(request, 'mainapp/print_sticker.html', context)


def find_patient_by_id(request):
    try:
        Patient.objects.get(id=request.GET.get('pid'))
    except Patient.DoesNotExist:
        return JsonResponse(data={}, status=404)

    return JsonResponse({})
