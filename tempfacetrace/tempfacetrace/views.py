from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.contrib.auth import login, authenticate, logout
from .models import Student, Attendance, Queries
from tempfacetrace.forms import RegistrationForm, AccountAuthenticationForm
from django.views.decorators.cache import never_cache
import datetime
import cv2
import face_recognition
import numpy as np


def register(request):
    user = request.user
    admins = Student.objects.filter(is_admin = True)
    admin_emails = [admin.email for admin in admins]
    if user.is_authenticated: 
        if user.email in admin_emails:
            return redirect('AdminDashboard')
        request.session.clear() 
        return redirect('Login')
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            student = authenticate(email = email, password = raw_password)
            login(request, student)
            return redirect('Student')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'register.html', context)

def loginuser(request):
    context = {}
    admins = Student.objects.filter(is_admin = True)
    admin_emails = [admin.email for admin in admins]
    user = request.user
    if user.is_authenticated:
        if user.email in admin_emails:
            return redirect('AdminDashboard') 
        return redirect("Student")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                if user.email in admin_emails:
                    return redirect('AdminDashboard')
                return redirect("Student")
    else:
        form = AccountAuthenticationForm()
    context['login_form'] = form
    return render(request, "login.html", context)



def logoutuser(request):
    request.session.clear()
    logout(request)
    return redirect("Login")

@never_cache
def adminDashboard(request):
    params =  fetchDomains(request)
    if request.POST:
        studentid1 = request.POST['studentid1']
        studentid2 = request.POST['studentid2']
        if (studentid1 == studentid2):
            students = Student.objects.all()
            studentid_list = [student.studentid for student in students]
            found = int(studentid1) in studentid_list
            if found:
                if not (Attendance.objects.filter(studentid = studentid1, date = str(datetime.date.today()))):
                    student = Student.objects.filter(studentid = studentid1)
                    student_present = Attendance(studentname = student[0].studentname, studentid = student[0].studentid, domain = student[0].domain, image = student[0].image if student[0].image else "", date = str(datetime.date.today()))
                    student_present.save()
    return render(request, 'index.html', {'details':params})

def fetchDomains(request):
    students = Student.objects.all()
    domainlist = [student.domain for student in students]
    domainlist = list(set(domainlist))
    defaultimg = '../media/images/man.png'
    student_domainwise = [[{'studentname': student.studentname, 'studentid': student.studentid, 'image':'../media/'+str(student.image) if student.image else defaultimg,'attendance':fetchAttendance(student.studentid)} for student in students if student.domain == domain] for domain in domainlist]
    params = []
    for i in range(0, len(domainlist)):
        lst = {}
        lst['domain_name'] = domainlist[i]
        lst['details'] = student_domainwise[i]
        params.append(lst)
    return params


def get_data(request):
    students = Student.objects.all()
    studentid_list = [student.studentid for student in students] # for checking if student is registered or not
    presentStudents = Attendance.objects.filter(date = str(datetime.date.today())) # for checking if the attendance is already taken or not
    presentStudentslist = [student.studentid for student in presentStudents]
    studentEmailandId = {student.email:student.studentid for student in students}
    params = {'studentid_list':studentid_list, 'present_student_list':presentStudentslist, 'student_email_studentid':studentEmailandId}
    return JsonResponse(params)

def userIsValid(request):
    email = request.GET.get('param1')
    password = request.GET.get('param2')
    user = authenticate(email=email, password=password)
    params = {'result':'True'} if (user==request.user) else {'result':'False'}
    return JsonResponse(params)
        

def student(request):
    user = request.user
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                studentid = user.studentid
                if not (Attendance.objects.filter(studentid = studentid, date = str(datetime.date.today()))):
                    student = Student.objects.filter(studentid = studentid)
                    student_present = Attendance(studentname = student[0].studentname, studentid = student[0].studentid, domain = student[0].domain, image = student[0].image if student[0].image else "", date = str(datetime.date.today()))
                    student_present.save()
    return render(request, 'normal-user.html', {'studentname':user.studentname})


def profile(request):
    user = request.user
    name = user.studentname
    id = user.studentid
    email = user.email
    domain = user.domain
    image = user.image if user.image else "../media/images/man.png"
    attended = Attendance.objects.filter(studentid = id)
    attended_list = [attended for attended in attended if (attended.date.strftime("%B") == datetime.date.today().strftime("%B"))]
    noOfDaysPresent = len(attended_list)
    noOfDaysPassed = datetime.date.today().day
    attendance_percent = "{:.2f}".format((noOfDaysPresent/noOfDaysPassed)*100)
    monthname = datetime.date.today().strftime("%B")
    params = {'name':name, 'id':id, 'email':email, 'domain':domain, 'attendance':attendance_percent, 'monthname':monthname, 'image':image}
    return render(request, 'profile.html', params)



def fetchAttendance(studentid):
    attended = Attendance.objects.filter(studentid = studentid)
    attended_list = [attended for attended in attended if (attended.date.strftime("%B") == datetime.date.today().strftime("%B"))]
    noOfDaysPresent = len(attended_list)
    noOfDaysPassed = datetime.date.today().day
    attendance_percent = "{:.2f}".format((noOfDaysPresent/noOfDaysPassed)*100)
    return attendance_percent



def queries(request):
    queries = list(Queries.objects.all())
    queries.reverse()
    return render(request, 'queries.html', {'queries':queries})

def sendQuery(request):
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email = email, password = password)
        if user:
            studentname = user.studentname
            studentid = user.studentid
            date = str(datetime.date.today())
            query = request.POST['querybox']
            querybox = Queries(studentname=studentname, studentid=studentid, date=date, query=query, image = user.image if user.image else "images/man.png")
            querybox.save()
    return render(request, 'send-query.html')


def face_attendance():
    camera = cv2.VideoCapture(0)
    Adarsh_image = face_recognition.load_image_file("media/images/21052130.jpg")
    Adarsh_face_encoding = face_recognition.face_encodings(Adarsh_image)[0]

    Sanu_image = face_recognition.load_image_file("media/images/101010.jpg")
    Sanu_face_encoding = face_recognition.face_encodings(Sanu_image)[0]

    known_face_encodings = [
        Adarsh_face_encoding,
        Sanu_face_encoding,
    ]
    known_face_names = [
        "Adarsh",
        "Sanu",
    ]
    known_face_studentids = [
        "21052130",
        "101010",
    ]
    # Initialize some variables
    face_locations = []
    face_encodings = []
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            frame = cv2.flip(frame, 1)
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # Only process every other frame of video to save time
           
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    studentid = known_face_studentids[best_match_index]
                    # print("Name: "+name+" Studentid: "+studentid)
                    students = Student.objects.all()
                    studentid_list = [student.studentid for student in students]
                    found = int(studentid) in studentid_list
                    if found:
                        if not (Attendance.objects.filter(studentid = studentid, date = str(datetime.date.today()))):
                            student = Student.objects.filter(studentid = studentid)
                            student_present = Attendance(studentname = student[0].studentname, studentid = student[0].studentid, domain = student[0].domain, image = student[0].image if student[0].image else "", date = str(datetime.date.today()))
                            student_present.save()
                        else:
                            name=known_face_names[best_match_index]+" -Attendance Taken!"
                # face_names.append(name)
            

            # Display the results
            for top, right, bottom, left in face_locations:
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (50, 205, 154), 2)

                # Draw a label with a name below the face
                # cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                # Calculate the width of the text
                text_width, _ = cv2.getTextSize(name, font, 1.0, 1)[0]

                # Calculate the position to center the text
                text_x = left + (right - left - text_width) // 2
                text_y = bottom + 36
                # Draw the text in the center
                cv2.putText(frame, name, (text_x, text_y), font, 1.0, (0, 0, 255), 1)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def video_feed(request):
    return StreamingHttpResponse(face_attendance(), content_type="multipart/x-mixed-replace;boundary=frame")