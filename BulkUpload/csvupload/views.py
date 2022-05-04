from curses import has_key
from time import sleep
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.views.generic.edit import FormView
from .functions import handle_uploaded_file
from csvupload.forms import UploadForm
from csvupload.models import Patient
from .tasks import file_read
from django.shortcuts import render, redirect
from .functions import recordcount


class CsvFileUpload(FormView):
    template_name = 'fileUpload.html'
    form_class = UploadForm
    model = Patient

    try:
        def post(self, request, *args, **kwargs):
            file = request.FILES['file']
            file_name = handle_uploaded_file(file)
            task = file_read.delay(file_name)
            totalrecords = recordcount(file_name)
            while not task.ready():
                if task.state == 'PENDING':
                    print("PROCESSING")
            if task.state == 'SUCCESS':
                print("COMPLETED")
            return redirect('patientlist', taskstatus=task.state, records=totalrecords)
    except Exception as e:
        print(e)
        import traceback
        traceback.print_exc()


class PatientList(FormView):
    template_name = 'patientList.html'
    model = Patient
    try:
        def get(self, request, *args, **kwargs):
            data = Patient.objects.all()
            taskstatus = kwargs.get('taskstatus')
            records = kwargs.get('records')
            recordsst = 'Total Records Read : '+records
            if taskstatus == 'SUCCESS':
                taskstatus = "FILE UPLOADED SUCCESSFULLY"
            elif taskstatus == 'PENDING':
                taskstatus = "FILE PROCESSING"
            elif taskstatus == 'FAILURE':
                taskstatus = "UPLOAD FAILED PLEASE CHECK THE FILE"
                data = {}
                recordsst = 'Total Records Read :0'
            patient_data = {
                "patient_list": data,
                "taskstate": taskstatus,
                "records": recordsst
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
