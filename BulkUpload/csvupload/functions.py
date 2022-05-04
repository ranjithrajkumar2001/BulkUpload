import csv
import json
from csvupload.models import Patient
from django.shortcuts import render

def handle_uploaded_file(f):
    print("Initiating")
    file_name = f.name
    try:
        with open('csvupload/csvfiles/' + file_name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return file_name
    except Exception as e:
        print(e)
        import traceback
        traceback.print_exc()


def recordcount(file_name):
    with open('csvupload/csvfiles/' + file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
        count = 0
        for row in reader:
            count += 1
    return count




