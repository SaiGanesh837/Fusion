
from django.conf.urls import url
from django.urls import path, include
from . import views


urlpatterns = [
    url(r'^registered_student_details/', views.fetch_student_details, name='fetch_student_details'),
    url(r'^update_grade/', views.update_grade, name='update_grade'), 
    url(r'^add_student/', views.add_student, name='add_student'),
    
]