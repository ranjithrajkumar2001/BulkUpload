import csv
from celery import shared_task
from csvupload.models import Patient
import datetime
from django.http import HttpResponse


@shared_task()
def file_read(file_name):
    try:
        with open('csvupload/csvfiles/' + file_name, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                patient_id = row['patient_id']
                first_name = row['first_name']
                last_name = row['last_name']
                email_address = row['email_address']
                date_of_birth = row['dob']
                eligible_for_insurance = row['eligible_for_insurance']
                created_datetime = datetime.datetime.now()

                p = Patient(patient_id=patient_id,
                            first_name=first_name,
                            last_name=last_name,
                            email_address=email_address,
                            date_of_birth=date_of_birth,
                            eligible_for_insurance=eligible_for_insurance,
                            created_datetime=created_datetime)

                p.save()
        return "COMPLETED"
    except Exception as e:
        print(e)
        return HttpResponse(e)
        import traceback
        traceback.print_exc()
