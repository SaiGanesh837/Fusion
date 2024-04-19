from datetime import datetime
from django.db.models.query_utils import Q
from django.http import request, HttpResponse
from django.shortcuts import get_object_or_404, render, HttpResponse, redirect
from django.http import HttpResponse, HttpResponseRedirect
import itertools
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse

# from applications.academic_information.models import Student
from applications.globals.models import (DepartmentInfo, Designation,
                                         ExtraInfo, Faculty, HoldsDesignation)

from applications.academic_procedures.models import (course_registration)
from applications.examination.models import (
    hidden_grades, authentication, grade)
from . import serializers
from datetime import date 
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response





@api_view(['GET', 'POST'])
def fetch_roll_of_courses(request):
    """
    This function is used to fetch roll numbers of students registered for a specific course.

    @variables:
        course_id - ID of the course for which roll numbers are being fetched
        working_year - Year for which roll numbers are being fetched
        obj - Queryset containing student registrations filtered by course ID and working year
        obj_serialized - Serialized data of student registrations
        resp - Dictionary containing the response data
    """
    if request.method == 'POST':
        # Retrieve the course_id and working_year from the request data
        course_id = request.data.get('course_id')
        working_year = request.data.get('working_year')

        if course_id is None:
            return Response({'error': 'Course ID is required in the request parameters'}, status=status.HTTP_400_BAD_REQUEST)

        # Filter students by the provided course ID and working year
        obj = course_registration.objects.filter(course_id=course_id , working_year=working_year)

        # Serialize the queryset
        obj_serialized = serializers.CourseRegistrationSerializer(
            obj, many=True).data

        # Prepare the response data
        resp = {
            'objt': obj_serialized
        }

        # Return the response
        return Response(data=resp, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Extract course_id from query parameters
        course_id = request.query_params.get('course_id')

        # Extract data for multiple students
        data_list = request.data

        # Check if course_id is provided
        if not course_id:
            return JsonResponse({'error': 'Course ID is required in the request parameters'}, status=status.HTTP_400_BAD_REQUEST)

        # Process each student in the list
        for data in data_list:
            student_id = data.get('student_id')
            grade = data.get('grade')

            # Check if student_id and grade are provided
            if not all([student_id, grade]):
                return JsonResponse({'error': 'Incomplete data provided for one of the students'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the entry already exists
        try:
            hidden_grade_obj = hidden_grades.objects.get(
                student_id=student_id, course_id=course_id)
            # If exists, update the grade
            hidden_grade_obj.grade = grade
            hidden_grade_obj.save()
        except hidden_grades.DoesNotExist:
            # If doesn't exist, create a new entry
            hidden_grade_obj = hidden_grades.objects.create(
                student_id=student_id,
                course_id=course_id,
                semester_id=semester_id,
                grade=grade
            )

        return Response({'message': 'Hidden grade added successfully'}, status=status.HTTP_201_CREATED)
    
@api_view(['POST'])
def enter_student_grades(request):
    if request.method == 'POST':
        # Extract data from the request
        data = request.data.get('grades', [])
        
        if not data:
            return Response({'error': 'No data provided'}, status=status.HTTP_400_BAD_REQUEST)

        for grade_data in data:
            student_id = grade_data.get('student_id')
            course_id = grade_data.get('course_id')
            semester_id = grade_data.get('semester_id')
            grade = grade_data.get('grade')

            if student_id is None or course_id is None or semester_id is None or grade is None:
                return Response({'error': 'Incomplete data provided'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                hidden_grade_obj = hidden_grades.objects.get(
                    student_id=student_id, 
                    course_id=course_id,
                    semester_id=semester_id
                )
                # If exists, update the grade
                hidden_grade_obj.grade = grade
                hidden_grade_obj.save()
            except hidden_grades.DoesNotExist:
                # If doesn't exist, create a new entry
                hidden_grade_obj = hidden_grades.objects.create(
                    student_id=student_id,
                    course_id=course_id,
                    semester_id=semester_id,
                    grade=grade
                )

        return Response({'message': 'Hidden grades added successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Unsupported method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
       

    
       


@api_view(['PATCH'])
def update_hidden_grade(request):
    course_id = request.query_params.get('course_id')
    student_id = request.query_params.get('student_id')

    if request.method == 'PATCH':
        # Check if the grade data is provided in the request
        if 'grade' in request.data:
            grade = request.data['grade']
            # Get the hidden grade object for the given course_id and student_id
            try:
                hidden_grade = hidden_grades.objects.get(
                    course_id=course_id, student_id=student_id)
                hidden_grade.grade = grade
                hidden_grade.save()
                return JsonResponse({'message': 'Grade updated successfully'}, status=200)
            except hidden_grades.DoesNotExist:
                return JsonResponse({'error': 'No hidden grade found for the provided course_id and student_id'}, status=404)
        else:
            return JsonResponse({'error': 'Incomplete data provided'}, status=400)
    else:
        return JsonResponse({'error': 'Unsupported method'}, status=405)


@api_view(['PATCH'])
def update_hidden_grade_multiple(request):
    if request.method == 'PATCH':
        # Check if the data is provided in the request
        if 'grades' in request.data:
            grades_data = request.data['grades']
            for grade_data in grades_data:
                course_id = grade_data.get('course_id')
                student_id = grade_data.get('student_id')
                semester_id = grade_data.get('semester_id')
                grade = grade_data.get('grade')

                if course_id is None or student_id is None or semester_id is None or grade is None:
                    return Response({'error': 'Incomplete data provided for one of the grades'}, status=400)

                # Get the hidden grade object for the given course_id, student_id, and semester_id
                try:
                    hidden_grade = hidden_grades.objects.get(
                        course_id=course_id, student_id=student_id, semester_id=semester_id)
                    hidden_grade.grade = grade
                    hidden_grade.save()
                except hidden_grades.DoesNotExist:
                    # If the grade doesn't exist, create a new one
                    hidden_grade = hidden_grades.objects.create(
                        course_id=course_id, student_id=student_id, semester_id=semester_id, grade=grade)
                    hidden_grade.save()

            return Response({'message': 'Grades updated successfully'}, status=200)
        else:
            return Response({'error': 'No grade data provided'}, status=400)
    else:
        return Response({'error': 'Unsupported method'}, status=405)


@api_view(['PATCH'])
def update_authenticator(request):
    if request.method == 'PATCH':
        # Extract year and authenticator number from the request
        year = request.data.get('year')
        authenticator_number = request.data.get('authenticator_number')

        # Validate year format
        try:
            datetime.strptime(year, '%Y')
        except ValueError:
            return Response({'error': 'Invalid year format. Please use YYYY format.'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve all authentication objects for the given year
        auth_objects = authentication.objects.filter(year__year=year)

        if not auth_objects.exists():
            return Response({'error': 'No authentication entries found for the provided year.'}, status=status.HTTP_404_NOT_FOUND)

        # Check if all three authenticators are verified for all authentication objects
        for auth_object in auth_objects:
            if not (auth_object.authenticator_1 and auth_object.authenticator_2 and auth_object.authenticator_3):
                return Response({'all_authenticated': False}, status=status.HTTP_200_OK)
        
        return Response({'all_authenticated': True}, status=status.HTTP_200_OK)






@api_view(['PATCH'])
def update_authenticator(request):
    """
    This function is used to update the status of an authenticator for a specific course and year.

    @variables:
        course_id - ID of the course for which authenticator status is being updated
        year - Year for which authenticator status is being updated
        authenticator_number - Number representing the authenticator whose status is being updated
        auth_objects - Queryset containing authentication objects filtered by year and course_id
        auth_object - Authentication object for the given year and course_id
    """
    if request.method == 'PATCH':
        # Extract course id, year, and authenticator number from the request
        course_id = int(request.data.get('course_id'))
        year = request.data.get('year')[:4]
        authenticator_number = int(request.data.get('authenticator_number'))
        
        # Validate year format
        print(course_id,year,authenticator_number)
        try:
            datetime.strptime(year, '%Y')
        except ValueError:
            return Response({'error': 'Invalid year format. Please use YYYY format.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Retrieve all authentication objects for the given year and course id
        auth_objects = authentication.objects.filter(year__year=year ,course_id=course_id)
        print(authentication.objects.all()[0])
        if not auth_objects.exists():
            return Response({'error': 'No authentication entries found for the provided year and course id.'}, status=status.HTTP_404_NOT_FOUND)

        # Toggle the specified authenticator for each authentication object
        for auth_object in auth_objects:
            if authenticator_number == 1:
                auth_object.authenticator_1 = not auth_object.authenticator_1
            elif authenticator_number == 2:
                auth_object.authenticator_2 = not auth_object.authenticator_2
            elif authenticator_number == 3:
                auth_object.authenticator_3 = not auth_object.authenticator_3
            else:
                return Response({'error': 'Invalid authenticator number'}, status=status.HTTP_400_BAD_REQUEST)

            auth_object.save()

        return Response({'message': f'Authenticator {authenticator_number} toggled successfully for the year {year}'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def publish_grade(request):
    """
    This function is used to publish grades for a course.

    @variables:
        course_id - ID of the course for which grades are being published
        auth_obj - Authentication object corresponding to the course_id
        hidden_grades_list - List of hidden grades for the given course
        hidden_grade - Hidden grade object in the hidden_grades_list
        existing_final_grade - Existing final grade object for the student and course
    """
    course_id = request.GET.get('course_id')
    auth_obj = authentication.objects.filter(course=course_id).first()

    if auth_obj:
        if auth_obj.authenticator_1 and auth_obj.authenticator_2 and auth_obj.authenticator_3:
            # Get hidden grades for the given course
            hidden_grades_list = hidden_grades.objects.filter(
                course_id=course_id)

            # Update final grades table
            for hidden_grade in hidden_grades_list:
                # Check if final grade already exists
                existing_final_grade = grade.objects.filter(
                    student_id=hidden_grade.student_id,
                    course_id=hidden_grade.course_id,
                    semester_id=hidden_grade.semester_id
                ).first()

                if not existing_final_grade:
                    # Create final grade only if it doesn't already exist
                    grade.objects.create(
                        student_id=hidden_grade.student_id,
                        course_id=hidden_grade.course_id,
                        semester_id=hidden_grade.semester_id,
                        grade=hidden_grade.grade
                    )

            return JsonResponse({'message': 'Grades are ready to publish'}, status=200)
        else:
            return JsonResponse({'error': 'Not all authenticators are True'}, status=400)
    else:
        return JsonResponse({'error': 'Authentication object not present'}, status=404)





@api_view(['POST', 'GET'])
def generate_transcript_form(request):
    """
    This function is used to generate a transcript form for students.

    @variables:
        programme - Programme selected for filtering students
        batch - Batch selected for filtering students
        specialization - Specialization selected for filtering students
        students - Queryset containing filtered students based on programme, batch, and specialization
        serialized_students - Serialized JSON string representing the filtered students
        students_data - Python object obtained by deserializing the JSON string
        programmes - List of distinct programme values from Student objects
        specializations - List of distinct specialization values from Student objects
        batches - List of distinct batch values from Student objects
        context - Dictionary containing programmes, batches, and specializations for rendering the form
    """
    if request.method == 'POST':
        programme = request.data.get('programme')
        batch = request.data.get('batch')
        specialization = request.data.get('specialization')
        print(programme, batch, specialization)

        if specialization is None:
            students = Student.objects.filter(programme=programme, batch=batch)
        else:
            students = Student.objects.filter(programme=programme, batch=batch, specialization=specialization)

        # Serialize QuerySet to JSON string
        serialized_students = serialize('json', students)
        print(serialized_students)
        # Deserialize JSON string to Python object
        students_data = json.loads(serialized_students)

        # Pass the deserialized data to JsonResponse
        return JsonResponse({'students': students_data})
    else:
        programmes = Student.objects.values_list('programme', flat=True).distinct()
        specializations = Student.objects.exclude(specialization__isnull=True).values_list('specialization', flat=True).distinct()
        batches = Student.objects.values_list('batch', flat=True).distinct()
        context = {
            'programmes': list(programmes),  
            'batches': list(batches),  
            'specializations': list(specializations),  
        }

        return JsonResponse(context)







@api_view(['POST', 'GET'])
def generate_transcript(request):
    """
    This function is used to generate a transcript for a student.

    @variables:
        student_id - ID of the student for whom the transcript is being generated
        semester - Semester for which the transcript is being generated
        student_grades - Queryset containing grades for the student in the specified semester
        transcript_data - List to hold transcript data for each course
        grade - Grade object for each course in the specified semester
        course_info - Dictionary containing course information to be included in the transcript
        student_info - Information about the student, such as CPI (Cumulative Performance Index)
        cpi - Cumulative Performance Index of the student
        course_detail - Details of the course obtained from Curriculum
    """
    if request.method == 'POST':
        student_id = request.data.get('student_id')
        semester = request.data.get('semester')
        
        # Fetch the courses and grades for the student in the specified semester
        student_grades = Student_grades.objects.filter(roll_no=student_id, semester=semester)
        print(student_id,semester)
        # Prepare data to be returned
        transcript_data = []
        for grade in student_grades:
            # Access fields of each object
            course_info = {
                'course_id': grade.course_id.course_name,
                'total_marks': grade.total_marks,
                'grade': grade.grade,
                'batch': grade.batch,
            }
            
            student_info = Student.objects.filter(id=student_id).first()
            print(student_info.cpi)
            if student_info:
                cpi = student_info.cpi
                course_info['cpi'] = cpi
            else:
                # Handle case where student info is not found
                print("cpi is not there")
                pass
            # Fetch course details from Curriculum
            course_detail = Curriculum.objects.filter(course_id=grade.course_id).first()
            if course_detail:
                # Include additional attributes
                course_info['course_code'] = course_detail.course_code
                course_info['credits'] = course_detail.credits
            else:
                # If course details not found, assign default values
                course_info['course_code'] = "Unknown"
                course_info['credits'] = 0
            
            transcript_data.append(course_info)
        
        return JsonResponse({'transcript': transcript_data})
    else:
        return JsonResponse({'error': 'Invalid request method'})





@api_view(['POST', 'GET'])
def get_curriculum_values(request):
    """
    This function is used to retrieve curriculum values for a given course.

    @variables:
        course_id - ID of the course for which curriculum values are being retrieved
        curriculum_values - Curriculum object corresponding to the course_id
    """
    try:
        course_id = request.data.get('course_id')
        
        curriculum_values = Curriculum.objects.get(course_id=course_id)
        print(Curriculum.objects.all())
        return JsonResponse({
            'course_code': curriculum_values.course_code,
            'credits': curriculum_values.credits,
            'course_type': curriculum_values.course_type,
            'programme': curriculum_values.programme,
            'branch': curriculum_values.branch,
            'sem': curriculum_values.sem,
            'optional': curriculum_values.optional,
            'floated': curriculum_values.floated
        })
    except Curriculum.DoesNotExist:
        print(Curriculum.objects.all())
        return JsonResponse({
            'course_code': 'Unknown',
            'credits': 0,
            'course_type': 'Unknown',
            'programme': 'Unknown',
            'branch': 'Unknown',
            'sem': 0,
            'optional': False,
            'floated': False
        })






@api_view(['POST', 'GET'])
def get_grade_for_course(course_id, batch, year, semester_id, selected_student_id):
    """
    This function is used to retrieve the grade for a specific course, batch, year, semester, and student.

    @parameters:
        course_id - ID of the course for which grade is being retrieved
        batch - Batch for which grade is being retrieved
        year - Year for which grade is being retrieved
        semester_id - ID of the semester for which grade is being retrieved
        selected_student_id - ID of the student for whom grade is being retrieved
    
    @variables:
        grades - Queryset containing grades filtered by course_id, batch, year, semester_id, and selected_student_id
    """
    # Filter Student_grades based on course_id, batch, year, semester_id, and selected_student_id
    grades = Student_grades.objects.filter(
        course_id=course_id,
        batch=batch,
        roll_no=selected_student_id,
        year=year,
        semester=semester_id,
    )

    # Assuming only one grade is expected for a given combination of parameters
    if grades.exists():
        return grades.first().grade
    else:
        return None  # Return None if no grade is found





@api_view(['POST', 'GET'])
def get_course_names(request):
    """
    This function is used to retrieve course names and IDs.

    @variables:
        courses - Queryset containing all Course objects
        course_data - List of dictionaries containing course IDs and names
    """
    if request.method == 'GET':
        # Retrieve all course names and IDs
        courses = Course.objects.all()
        course_data = [{'id': course.id, 'name': course.course_name} for course in courses]
        
        if not course_data:
            return JsonResponse({'error': 'No courses found.'}, status=status.HTTP_404_NOT_FOUND)
        
        return JsonResponse({'courses': course_data}, status=status.HTTP_200_OK)





@api_view(['POST'])
def add_courses(request):
    """
    This function is used to add courses along with authentication objects.

    @variables:
        courses - List of courses received from the request body
        created_authentications - List to hold the created authentication objects
        course_instance - Instance of the Course model corresponding to the course ID
        authentication_object - Authentication object created for the course
        serialized_data - Serialized data of the created authentication objects
    """
    if request.method == 'POST':
        # Get the list of courses from the request body
        courses = request.data.get('courses', [])

        # Create a list to hold the created authentication objects
        created_authentications = []

        # Iterate over the list of courses and create an authentication object for each
        for course in courses:
            try:
                # Get the Course instance corresponding to the course ID
                course_instance = Course.objects.get(id=course['id']) 
                
                # Create a new authentication object with the Course instance
                authentication_object = authentication.objects.create(course_id=course_instance)
                
                # Append the created authentication object to the list
                created_authentications.append(authentication_object)
            except Exception as e:
                # Handle any errors that occur during object creation
                # You can choose to log the error or handle it based on your requirements
                print(f"Error creating authentication object for course ID {course['id']}: {e}")
        
        # Convert the created authentication objects to dictionaries
        serialized_data = [{'id': obj.id, 'authenticator_1': obj.authenticator_1, 'authenticator_2': obj.authenticator_2, 'authenticator_3': obj.authenticator_3, 'year': obj.year.year, 'course_id': obj.course_id_id} for obj in created_authentications]
        
        # Return a JSON response with the serialized data
        return JsonResponse(serialized_data, status=201, safe=False)





@api_view(['PATCH'])
def update_grades(request):
    """
    This function is used to update grades for students.

    @variables:
        updated_students_data - JSON data containing updated grades for students
        roll_no - Roll number of the student
        course_id - ID of the course for which grades are being updated
        semester_id - ID of the semester for which grades are being updated
        year - Year for which grades are being updated
        grade - Updated grade received by the student
        total_marks - Updated total marks obtained by the student
        student_grade_obj - Student grades object to be updated or created
        created - Flag indicating whether a new student grade object was created
    """
    if request.method == 'PATCH':
        try:
            # Extract the updated student data from the request body
            updated_students_data = json.loads(request.body)
            print(updated_students_data)
            # Iterate over each updated student data
            for student_data in updated_students_data:
                roll_no = student_data.get('roll_no')
                course_id = int(student_data.get('course_id'))
                semester_id = student_data.get('semester_id')
                year = int(student_data.get('year'))
                grade = student_data.get('grade')
                total_marks = student_data.get('total_marks')

                # Check if all necessary data is provided
                if not (roll_no and course_id and semester_id and year and grade and total_marks):
                    return JsonResponse({'error': 'Incomplete data provided'}, status=400)

                # Update the student grade
                student_grade_obj, created = Student_grades.objects.update_or_create(
                    roll_no=roll_no,
                    course_id=course_id,
                    semester=semester_id,
                    year=year,
                    defaults={'grade': grade, 'total_marks': total_marks}
                )

            return JsonResponse({'message': 'Student grades updated successfully'}, status=200)
        
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        
        except KeyError as e:
            return JsonResponse({'error': 'Missing required field: ' + str(e)}, status=400)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)





@api_view(['PATCH'])
def submit_grades(request):
    """
    This function is used to submit grades for students.

    @variables:
        updated_students_data - JSON data containing updated grades for students
        roll_no - Roll number of the student
        course_id - ID of the course for which grades are being submitted
        semester_id - ID of the semester for which grades are being submitted
        year - Year for which grades are being submitted
        grade - Grade received by the student (defaulted to 'NA')
        total_marks - Total marks obtained by the student (defaulted to 0)
        course - Course object corresponding to course_id
        student_grade_obj - Student grades object to be updated or created
        created - Flag indicating whether a new student grade object was created
    """
    if request.method == 'PATCH':
        try:
            updated_students_data = json.loads(request.body)
            print(updated_students_data)

            for student_data in updated_students_data:
                roll_no = student_data.get('roll_no')
                course_id = int(student_data.get('course_id'))
                semester_id = student_data.get('semester_id')
                year = int(student_data.get('year'))
                grade = student_data.get('grade','NA')
                total_marks = student_data.get('total_marks','0')

                if not (roll_no and course_id and semester_id and year and grade and total_marks):
                    return JsonResponse({'error': 'Incomplete data provided'}, status=400)

                # Retrieve the Course object based on course_id
                course = Course.objects.get(id=course_id)

                # Update or create the student grade object
                student_grade_obj, created = Student_grades.objects.update_or_create(
                    roll_no=roll_no,
                    course_id=course,  # Use the Course object instead of course_id
                    semester=semester_id,
                    year=year,
                    defaults={'grade': grade, 'total_marks': total_marks}
                )

            return JsonResponse({'message': 'Student grades updated successfully'}, status=200)
        
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        
        except KeyError as e:
            return JsonResponse({'error': 'Missing required field: ' + str(e)}, status=400)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)




@api_view(['POST', 'GET'])
def get_registered_students_roll_no(request):
    """
    This function is used to retrieve registered students' information for a particular course and year.

    @variables:
        course_id - ID of the course for which registrations are being retrieved
        year - Year for which registrations are being retrieved
        registrations - Queryset containing course registrations filtered by course_id and year
        data - List to store serialized student data
        student_data - Dictionary to store individual student information
        student_grade - Grade and total marks of the student for the specified course
    """
    # Retrieve the course_id and year from the request query parameters
    course_id = request.data.get('course_id')
    year = request.data.get('year')
    
    if not course_id or not year:
        return JsonResponse({'error': 'Course ID and year are required'}, status=400)

    try:
        # Filter course registrations by course_id and year
        registrations = Register.objects.filter(curr_id=course_id, year=year)
        # Serialize the queryset
        data = []
        for registration in registrations:
            # Access fields of the related Student instance
            student_data = {
                'roll_no': registration.student_id.id.user.username,
                'name': registration.student_id.id.user.first_name,  # Assuming first_name is a field of the User model
                'email': registration.student_id.id.user.email,  # Assuming email is a field of the User model
                # Include other relevant fields from the Student model
                'grade': None,
                'marks': None
            }
            
            # Retrieve grades and total marks for the student
            try:
                print(registration.student_id.id , course_id)
                student_grade = Student_grades.objects.get(roll_no=student_data['roll_no'],course_id=course_id)
                student_data['grade'] = student_grade.grade
                student_data['marks'] = student_grade.total_marks
                
                print(student_grade)
            except Student_grades.DoesNotExist:
                print("Didn't find grades for roll_no:", registration.student_id.id, "and course_id:", course_id)
                pass
            print(student_data)
            data.append(student_data)
        # Return the serialized data in the response
        return JsonResponse({'registrations': data}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)





@api_view(['POST', 'GET'])
def get_to_request(username):
    """
    This function is used to get requests for the receiver

    @variables:
        req - Contains request queryset

    """
    req = SpecialRequest.objects.filter(request_receiver=username)
    return req




@api_view(['POST', 'GET'])
def browse_announcements():
    """
    This function is used to browse Announcements Department-Wise
    made by different faculties and admin.

    @variables:
        cse_ann - Stores CSE Department Announcements
        ece_ann - Stores ECE Department Announcements
        me_ann - Stores ME Department Announcements
        sm_ann - Stores SM Department Announcements
        all_ann - Stores Announcements intended for all Departments
        context - Dictionary for storing all above data

    """
    cse_ann = Announcements.objects.filter(department="CSE")
    ece_ann = Announcements.objects.filter(department="ECE")
    me_ann = Announcements.objects.filter(department="ME")
    sm_ann = Announcements.objects.filter(department="SM")
    all_ann = Announcements.objects.filter(department="ALL")

    context = {
        "cse" : cse_ann,
        "ece" : ece_ann,
        "me" : me_ann,
        "sm" : sm_ann,
        "all" : all_ann
    }

    return context




@api_view(['POST', 'GET'])
def announce(request):
    """
    This function is used to make announcements by faculty or admin.

    @variables:
        usrnm - Current user's username
        user_info - Extra information of the current user
        ann_maker_id - ID of the user making the announcement
        batch - Batch for which the announcement is intended
        programme - Programme for which the announcement is intended
        message - Content of the announcement
        upload_announcement - File uploaded with the announcement
        department - Department for which the announcement is intended
        ann_date - Date of the announcement
        getstudents - All users with extra information
        
    """
    usrnm = get_object_or_404(User, username=request.user.username)
    user_info = ExtraInfo.objects.all().select_related('user', 'department').filter(user=usrnm).first()
    ann_maker_id = user_info.id
    
    if request.method == 'POST':
        batch = request.data.get('batch', '')
        programme = request.data.get('programme', '')
        message = request.data.get('announcement', '')
        upload_announcement = request.FILES.get('upload_announcement')
        department = request.data.get('department', 'ALL')
        ann_date = datetime.today()
        user_info = ExtraInfo.objects.all().select_related('user', 'department').get(id=ann_maker_id)
        getstudents = ExtraInfo.objects.select_related('user')
        
        obj1, created = Announcements.objects.get_or_create(maker_id=user_info,
                                                            batch=batch,
                                                            programme=programme,
                                                            message=message,
                                                            upload_announcement=upload_announcement,
                                                            department=department,
                                                            ann_date=ann_date)

        response_data = {
            'status': 'success',
            'message': 'Announcement successfully created'
        }
        return JsonResponse(response_data)
    else:
        response_data = {
            'error': 'Invalid request method'
        }
        return JsonResponse(response_data, status=405)
