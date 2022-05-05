from django.views.generic.edit import FormView
from .functions import handle_uploaded_file
from csvupload.forms import UploadForm
from csvupload.models import Patient
from .tasks import file_read
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse


class CsvFileUpload(FormView):
    template_name = 'fileUpload.html'
    form_class = UploadForm
    model = Patient

    def post(self, request, *args, **kwargs):
        try:
            file = request.FILES['file']
            file_name = handle_uploaded_file(file)
            task = file_read.delay(file_name)
            print(task)
            while not task.ready():
                if task.state == 'PENDING':
                    print("PROCESSING")
            if task.state == 'SUCCESS':
                print("COMPLETED")
                return redirect('patientlist')
            if task.state == 'FAILURE':
                return redirect('csvfileupload')

        except Exception as e:
            import traceback
            traceback.print_exc()


class PatientList(FormView):
    template_name = 'patientList.html'
    model = Patient
    try:
        def get(self, request, *args, **kwargs):
            records_count = Patient.objects.all().count()
            data = Patient.objects.all().order_by('first_name')
            paginator = Paginator(data, 10)
            page_number = request.GET.get('page')
            final_data = paginator.get_page(page_number)
            patient_data = {
                "patient_list": final_data,
                "records_count": records_count
            }
            return render(request, self.template_name, patient_data)

        def post(self, request, *args, **kwargs):
            dummy = {}
            patient_data = {
                "patient_list": dummy
            }
            if request.POST['search']:
                field = request.POST['fieldnames']
                if field == 'firstname':
                    data = request.POST['search']
                    dummy = Patient.objects.filter(first_name=data).values()
                    patient_data = {
                        "patient_list": dummy
                    }
                elif field == 'lastname':
                    data = request.POST['search']
                    dummy = Patient.objects.filter(last_name=data).values()
                    patient_data = {
                        "patient_list": dummy
                    }
                elif field == 'patientid':
                    data = request.POST['search']
                    dummy = Patient.objects.filter(patient_id=data).values()
                    patient_data = {
                        "patient_list": dummy
                    }
                elif field == 'emailaddress':
                    data = request.POST['search']
                    dummy = Patient.objects.filter(email_address=data).values()
                    patient_data = {
                        "patient_list": dummy
                    }
                elif field == 'eligibleforinsurance':
                    data = request.POST['search']
                    dummy = Patient.objects.filter(eligible_for_insurance=data).values()
                    patient_data = {
                        "patient_list": dummy
                    }
                elif field == 'dateofbirth':
                    data = request.POST['search']
                    dummy = Patient.objects.filter(date_of_birth=data).values()
                    patient_data = {
                        "patient_list": dummy
                    }
            else:
                firstname = request.POST['firstname']
                lastname = request.POST['lastname']
                dob = request.POST['dateofbirth']
                insurance = request.POST['insurance']
                if firstname != '' and lastname != '' and dob != '' and insurance != '':
                    dummy = Patient.objects.filter(first_name=firstname, last_name=lastname, date_of_birth=dob,
                                                   eligible_for_insurance=insurance).values()
                    patient_data = {"patient_list": dummy
                                    }
                elif firstname == '' and lastname == '' and dob == '':
                    dummy = Patient.objects.filter(eligible_for_insurance=insurance).values()
                    patient_data = {"patient_list": dummy
                                    }
                elif firstname == '' and lastname == '' and insurance == '':
                    dummy = Patient.objects.filter(date_of_birth=dob).values()
                    patient_data = {"patient_list": dummy
                                    }
                elif firstname == '' and dob == '' and insurance == '':
                    dummy = Patient.objects.filter(last_name=lastname).values()
                    patient_data = {"patient_list": dummy
                                    }
                elif lastname == '' and dob == '' and insurance == '':
                    dummy = Patient.objects.filter(first_name=firstname).values()
                    patient_data = {"patient_list": dummy
                                    }
                elif firstname == '' and lastname == '':
                    dummy = Patient.objects.filter(date_of_birth=dob, eligible_for_insurance=insurance).values()
                    patient_data = {"patient_list": dummy
                                    }
                elif firstname == '' and dob == '':
                    dummy = Patient.objects.filter(last_name=lastname, eligible_for_insurance=insurance).values()
                    patient_data = {"patient_list": dummy
                                    }
                elif firstname == '' and insurance == '':
                    dummy = Patient.objects.filter(last_name=lastname, date_of_birth=dob).values()
                    patient_data = {"patient_list": dummy
                                    }
                elif lastname == '' and dob == '':
                    dummy = Patient.objects.filter(first_name=firstname, eligible_for_insurance=insurance).values()
                    patient_data = {"patient_list": dummy
                                    }
                elif lastname == '' and insurance == '':
                    dummy = Patient.objects.filter(first_name=firstname, date_of_birth=dob).values()
                    patient_data = {"patient_list": dummy
                                    }
                elif firstname == '':
                    dummy = Patient.objects.filter(last_name=lastname, date_of_birth=dob,
                                                   eligible_for_insurance=insurance).values()
                    patient_data = {"patient_list": dummy
                                    }
                elif lastname == '':
                    dummy = Patient.objects.filter(first_name=firstname, date_of_birth=dob,
                                                   eligible_for_insurance=insurance).values()
                    patient_data = {"patient_list": dummy
                                    }
                elif dob == '':
                    dummy = Patient.objects.filter(first_name=firstname, last_name=lastname,
                                                   eligible_for_insurance=insurance).values()
                    patient_data = {"patient_list": dummy
                                    }
                elif insurance == '':
                    dummy = Patient.objects.filter(first_name=firstname, last_name=lastname, date_of_birth=dob).values()
                    patient_data = {"patient_list": dummy
                                    }
            return render(request, 'search.html', patient_data)
    except Exception as e:
        print(e)
        import traceback
        traceback.print_exc()
