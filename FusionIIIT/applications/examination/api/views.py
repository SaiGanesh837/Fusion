from django.db.models.query_utils import Q
from django.http import request,HttpResponse
from django.shortcuts import get_object_or_404, render, HttpResponse,redirect
from django.http import HttpResponse, HttpResponseRedirect
import itertools
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse

from applications.academic_procedures.models import(course_registration)

from . import serializers
from applications.examination.models import(hidden_grades)

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response



@api_view(['GET'])
def fetch_student_details(request):
    if request.method == 'GET':
        # obj=course_registration.objects.filter(course_id__id=course_id, student_id__batch=batch)
        student_obj=course_registration.objects.all()
        student_serialized = serializers.CourseRegistrationSerializer(student_obj , many=True).data
        resp = {
            'objt' : student_serialized
        }

        return Response(data=resp , status=status.HTTP_200_OK)
    


@api_view(['POST'])
def update_grade(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        course_id = request.POST.get('course_id')
        new_grade = request.POST.get('grade')

        private_grade = get_object_or_404(private_grade, student_id=student_id, course_id=course_id)
        private_grade.grade = new_grade
        private_grade.save()

        return JsonResponse({'message': 'Grade updated successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def add_student(request):
    if request.method == 'POST':
        # Assuming the POST request contains necessary data for a new student
        student_id = request.POST.get('student_id')
        course_id = request.POST.get('course_id')
        semester_id = request.POST.get('semester_id')
        grades = request.POST.get('grades')

        # Create a new private_grade object
        new_student = hidden_grades.objects.create(
            student_id=student_id,
            course_id=course_id,
            semester_id=semester_id,
            grades=grades
        )

        return JsonResponse({'message': 'Student added successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)




































# @login_required(login_url='/accounts/login')
# def exam(request):
#     """
#     This function is used to Differenciate acadadmin and all other user.

#     @param:
#         request - contains metadata about the requested page

#     @variables:
#         user_details - Gets the information about the logged in user.
#         des - Gets the designation about the looged in user.
#     """
#     user_details = ExtraInfo.objects.get(user = request.user)
#     des = HoldsDesignation.objects.all().filter(user = request.user).first()
#     if str(des.designation) == "Associate Professor" or str(des.designation) == "Professor" or str(des.designation) == "Assistant Professor" :
#         return HttpResponseRedirect('/examination/submit/')
#     elif str(request.user) == "acadadmin" :
#         return HttpResponseRedirect('/examination/submit/')
    
#     return HttpResponseRedirect('/dashboard/')

# @login_required(login_url='/accounts/login')


# def submit(request):
    
#     return render(request,'../templates/examination/submit.html' , {})

# @login_required(login_url='/accounts/login')
# def verify(request):
#     return render(request,'../templates/examination/verify.html' , {})

# @login_required(login_url='/accounts/login')      
# def publish(request):
#     return render(request,'../templates/examination/publish.html' ,{})


# @login_required(login_url='/accounts/login')
# def notReady_publish(request):
#     return render(request,'../templates/examination/notReady_publish.html',{})