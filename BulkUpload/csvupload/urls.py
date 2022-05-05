from django.contrib import admin
from django.urls import path
from csvupload import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.CsvFileUpload.as_view(),name='csvfileupload'),
    path('patientlist/',views.PatientList.as_view(), name='patientlist'),
]