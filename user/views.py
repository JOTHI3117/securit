from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from client import encrypt
from django.conf import settings
import base64
import re
from center.models import *


# Create your views here.


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            users = User.objects.get(email=email)
            if users.password == password:
                request.session['user'] = users.email
                messages.success(request, 'Login Successfully')
                return redirect('/user_main')
            else:
                messages.success(request, 'password is wrong')
                return redirect('/user_login')
        except User.DoesNotExist:
            messages.success(request, 'Email id does not exist')
            return redirect('/user_login')
    return render(request, 'user/login.html')


def user_register(request):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[gmail]+(\.[A-Z|a-z]{2,})+')
    if request.method == "POST":
        reg = User()
        reg.name = request.POST.get('name')
        reg.email = request.POST.get('email')
        reg.password = request.POST.get('password')
        if re.fullmatch(regex, reg.email):
            try:
                main = User.objects.get(email=reg.email)
                messages.success(request, 'Email id Already Exits')
                return redirect('/user_register')
            except:
                reg.save()
                messages.success(request, 'Register Successfully')
                return redirect('/user_login')
        else:
            messages.success(request, 'Invalid  Email-ID')
            return redirect('/user_register')
    return render(request, 'user/register.html')


def user_main(request):
    if 'user' in request.session:
        return render(request, 'user/user_main.html')
    else:
        return redirect('/user_login')


def user_logout(request):
    request.session.pop('user', None)
    messages.success(request, 'Logout Successfully')
    return redirect('/')


def company_details(request):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[gmail]+(\.[A-Z|a-z]{2,})+')
    if 'user' in request.session:
        name = User.objects.get(email=request.session['user'])
        if request.method == "POST":
            upload = Company_Details()
            upload.name = name.name
            upload.email = name.email
            upload.company_name = request.POST.get('company_name')
            upload.company_email = request.POST.get('company_email')
            upload.contact = request.POST['mobile']
            upload.address = request.POST.get('address')
            if re.fullmatch(regex, upload.company_email):
                try:
                    company = Company_Details.objects.get(company_email=upload.company_email)
                    messages.success(request, 'Email id already exist')
                    return redirect('/company_details')
                except:
                    upload.save()
                    messages.success(request, 'Company Details Upload Successfully')
                    return redirect('/user_main')
            else:
                messages.success(request, 'Invalid Email-Id')
                return redirect('/company_details')
        return render(request, 'user/company_details.html', {'name': name.name})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/user_login')


def view_director(request):
    if 'user' in request.session:
        user = Company_Details.objects.get(email=request.session['user'])
        return render(request, 'user/view_director.html', {'i': user})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/user_login')


def file_details(request, id):
    if 'user' in request.session:
        user = Company_Details.objects.get(id=id)
        if request.method == 'POST':
            name = File_Details()
            name.company_email = user
            name.email = request.session['user']
            name.file_name = request.POST.get('file_name')
            name.file_format = request.POST.get('file_format')
            name.file_weight = request.POST.get('file_weight')
            name.name = user.name
            print(name.file_name)
            name.save()
            messages.success(request, 'File-Format Upload Successfully')
            return redirect('/user_main')
        return render(request, 'user/file_format.html', {'name': user.approve, 'id': user.id})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/user_login')


def approve_file(request):
    if 'user' in request.session:
        user = File_Details.objects.filter(email=request.session['user'])
        messages.success(request, 'View Price list')
        return render(request, 'user/file_main.html', {'name': user})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/user_login')


def price_accept(request, id):
    if 'user' in request.session:
        user = File_Details.objects.get(id=id)
        user.accept_amount = True
        user.save()
        messages.success(request, 'Accept Price')
        return redirect('/approve_file')
    else:
        messages.success(request, 'Session Expired')
        return redirect('/user_login')


def price_deny(request, id):
    if 'user' in request.session:
        user = File_Details.objects.get(id=id).delete()
        messages.success(request, 'Deny Price')
        return redirect('/approve_file')
    else:
        messages.success(request, 'Session Expired')
        return redirect('/user_login')


def file_upload(request, id):
    if 'user' in request.session:
        user = File_Details.objects.get(id=id)
        if request.method == 'POST':
            user.file = request.FILES['file']
            user.files = True
            user.save()
            messages.success(request, 'File Upload Successfully')
            return redirect('/approve_file')
        return render(request, 'user/file_upload.html', {'name': user.id})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/user_login')


def requests_file(request, id):
    if 'user' in request.session:
        user = File_Details.objects.get(id=id)
        name = Request_File()
        name.request = user
        name.name = user.name
        name.email = request.session['user']
        name.save()
        messages.success(request, 'Send Request Successfully')
        return redirect('/approve_file')
    else:
        messages.success(request, 'Session Expired')
        return redirect('/user_login')


def data_send(request):
    if 'user' in request.session:
        user = Request_File.objects.filter(email=request.session['user'])
        messages.success(request, 'User requested file')
        return render(request, 'user/request_file.html', {'name': user})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/user_login')


def view_decrypt_file(request, id):
    if 'user' in request.session:
        user = Request_File.objects.get(id=id)
        files = user.request.file
        generator_key = user.request.secure_key
        if request.method == 'POST':
            key = request.POST.get('keys')
            keys = key.encode()
            keys = base64.b64encode(keys)
            if key == generator_key:
                response = encrypt.decrypt_file(f'{settings.MEDIA_ROOT}/{files}', keys)
                messages.success(request, 'File Download')
                user.download = True
                user.save()
                return response
            else:
                messages.success(request, 'Please File Correct Key')
            return redirect('/data_send')
        return render(request, 'user/decrypt_file.html', {'name': user.request.company_email.name, 'email': user.email,
                                                          'location': user.request.company_email.address,
                                                          'phone': user.request.company_email.contact,
                                                          'company_email': user.request.company_email.company_email,
                                                          'n_email': user.email,
                                                          'project': user.request.file_name})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/user_login')


def view_user_question(request):
    if 'user' in request.session:
        user = Company_Details.objects.filter(email=request.session['user'])
        messages.success(request, 'Upload client question and answer')
        return render(request, 'user/view_user_question.html', {'name': user})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/user_login')


def question(request):
    if 'user' in request.session:
        user = Company_Details.objects.get(email=request.session['user'])
        if request.method == 'POST':
            ques = Question()
            ques.one = request.POST.get('one')
            ques.two = request.POST.get('two')
            ques.three = request.POST.get('three')
            ques.four = request.POST.get('four')
            ques.five = request.POST.get('five')
            ques.email = request.session['user']
            ques.save()
            user.question = True
            user.save()
            return redirect('/view_user_question')
        return render(request, 'user/user_question.html',
                      {'name': user.name, 'email': user.email, 'company': user.company_name, 'mobile': user.contact,
                       'location': user.address})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/user_login')


def view_question(request):
    if 'user' in request.session:
        user = Question.objects.get(email=request.session['user'])
        messages.success(request, 'View our upload answer')
        return render(request, 'user/view_question.html',
                      {'one': user.one, 'two': user.two, 'three': user.three, 'four': user.four, 'five': user.five})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/user_login')


########################################################################
def client_request(request):
    if 'user' in request.session:
        user = Client_Request.objects.filter(user_email=request.session['user'])
        messages.success(request, 'View partner request')
        return render(request, 'user/client_request.html', {'name': user})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/user_login')


def client_accept(request, id):
    if 'user' in request.session:
        user = Client_Request.objects.get(id=id)
        user.accept = True
        user.save()
        messages.success(request, 'Accept Client')
        return redirect('/client_request')
    else:
        messages.success(request, 'Session Expired')
        return redirect('/user_login')


def client_deny(request, id):
    if 'user' in request.session:
        user = Client_Request.objects.get(id=id).delete()
        messages.success(request, 'Deny Client')
        return redirect('/client_request')
    else:
        messages.success(request, 'Session Expired')
        return redirect('/user_login')


def send_link(request, id):
    if 'user' in request.session:
        user = Client_Request.objects.get(id=id)
        user.send_link = True
        user.save()
        messages.success(request, 'Send Question Link')
        return redirect('/client_request')
    else:
        messages.success(request, 'Session Expired')
        return redirect('/user_login')


def view_change_client(request):
    if 'user' in request.session:
        user = Change_Mac.objects.filter(email=request.session['user'])
        messages.success(request, 'View requested client')
        return render(request, 'user/view_change_client.html', {'name': user})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/user_login')


def approve(request, id):
    if 'user' in request.session:
        user = Change_Mac.objects.get(id=id)
        user.approve = True
        user.save()
        messages.success(request, 'Approve Successfully')
        return redirect('/view_change_client')
    else:
        messages.success(request, 'Session Expired')
        return redirect('/user_login')


def deny(request, id):
    if 'user' in request.session:
        user = Change_Mac.objects.get(id=id).delete()
        messages.success(request, 'Deny Successfully')
        return redirect('/view_change_client')
    else:
        messages.success(request, 'Session Expired')
        return redirect('/user_login')
