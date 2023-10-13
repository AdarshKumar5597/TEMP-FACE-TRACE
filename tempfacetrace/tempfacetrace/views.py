from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate, logout
from .models import Student, Attendance, Queries
from tempfacetrace.forms import RegistrationForm, AccountAuthenticationForm
from django.views.decorators.cache import never_cache
import datetime


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