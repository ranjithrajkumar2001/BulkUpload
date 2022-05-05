# BulkUpload
Reading and storing data from CSV files using Django, Celery


**Steps to setup your localsystem:**

#Create Virtual Environment:

    python -m venv env

#Install the requirement.txt file

    pip install -r requirement.txt

#Activate Virtual Environment:

    source env/bin/activate
    
#Run the Server:

    python manage.py runserver
    
#start redis:

    redis-server --port 6369

#start Celery:

    celery -A myproject worker -l INFO
 
#Server

    http://127.0.0.1:8000/
    
#DB SCHEMA

    1.Database name : patient_db
    2.Table structure
      Patient Id
      First name 
      Last name
      Email address-(Unique)
      Date of Birth
      Eligible for Insurance (Yes/No) 
      Created Datetime
      Pk->UUID


    
