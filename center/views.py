from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from user.models import *
from . import encrypt
from django.conf import settings
import random, base64
import string
from django.core.mail import send_mail
from client.models import *
import re


# Create your views here.


def center_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            users = Center.objects.get(email=email)
            if users.password == password:
                request.session['center'] = users.email
                messages.success(request, 'Login Successfully')
                return redirect('/center_user')
            else:
                messages.success(request, 'password is wrong')
                return redirect('/center_login')
        except Center.DoesNotExist:
            messages.success(request, 'Email id does not exist')
            return redirect('/center_login')
    return render(request, 'center/login.html')


def center_register(request):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[gmail]+(\.[A-Z|a-z]{2,})+')
    if request.method == "POST":
        reg = Center()
        reg.name = request.POST.get('name')
        reg.email = request.POST.get('email')
        reg.password = request.POST.get('password')
        if re.fullmatch(regex, reg.email):
            try:
                center = Center.objects.get(email=reg.email)
                messages.success(request, 'Email id does not exits')
                return redirect('/center_register')
            except:
                reg.save()
                messages.success(request, 'Register Successfully')
                return redirect('/center_login')
        else:
            messages.success(request, 'Invalid Email-id')
            return redirect('/center_register')
    return render(request, 'center/register.html')


def center_user(request):
    if 'center' in request.session:
        return render(request, 'center/center_user.html')
    else:
        return redirect('/center_login')


def center_logout(request):
    request.session.pop('center', None)
    messages.success(request, 'Logout Successfully')
    return redirect('/')


def view_director_user(request):
    if 'center' in request.session:
        user = Company_Details.objects.filter(approve=True)
        messages.success(request, 'Director acceptance user')
        return render(request, 'center/view_director_user.html', {'name': user})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/center_login')


def view_director_send(request, id):
    if 'center' in request.session:
        company = Company_Details.objects.get(id=id)
        user = File_Details.objects.filter(email=company.email, send_data=True)
        messages.success(request, 'User file list')
        return render(request, 'center/director_send.html', {'name': user})
    else:
        return redirect('/center_login')


def encrypt_file(request, id):
    if 'center' in request.session:
        user = File_Details.objects.get(id=id)
        file = user.file
        keys = ''.join(random.choices(string.digits + string.ascii_letters, k=12))
        key = base64.b64encode(keys.encode())
        new = encrypt.encrypt_file(f'{settings.MEDIA_ROOT}/{file}', key)
        user.encrypt = True
        user.secure_key = keys
        user.save()
        messages.success(request, 'File Encrypt Successfully')
        return redirect('/view_director_user')
    else:
        return redirect('/center_login')


def director_user_accept(request):
    if 'center' in request.session:
        user = Company_Details.objects.filter(approve=True)
        messages.success(request, 'Director acceptance user')
        return render(request, 'center/director_user_accept.html', {'name': user})
    else:
        return redirect('/center_login')


def user_request(request, id):
    if 'center' in request.session:
        company = Company_Details.objects.get(id=id)
        try:
            user = Request_File.objects.filter(email=company.email)
            messages.success(request, 'User request')
            return render(request, 'center/user_request.html', {'name': user})
        except Request_File.DoesNotExist:
            messages.success(request, 'User not sent request')
            return redirect('/director_user_accept')
    else:
        return redirect('/center_login')


def generator_key(request, id):
    if 'center' in request.session:
        user = Request_File.objects.get(id=id)
        secure_key = user.request.secure_key
        user.generator_key = secure_key
        user.accept = True
        user.save()
        subject = 'It is very Secure'
        message = f'Key Generate,... {secure_key}, Do not share any one'
        from_email = 'virualmachine123@gmail.com'
        to_email = [user.email]
        res = send_mail(subject, message, from_email, to_email)
        if res == 1:
            messages.info(request, 'Mail send Successfully')
        else:
            messages.info(request, 'Sorry,could not send mail')
        return redirect('/director_user_accept')
    else:
        return redirect('/center_login')


def view_director_accept(request):
    if 'center' in request.session:
        user = Company_Details.objects.filter(approve=True)
        messages.success(request, 'Director acceptance user')
        return render(request, 'center/view_director_accept.html', {'name': user})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/center_user')


def view_client_request(request, id):
    if 'center' in request.session:
        user = Company_Details.objects.get(id=id)
        center = Requests_Client.objects.filter(email=user.email)
        messages.success(request, 'Requested Client')
        return render(request, 'center/view_client_request.html', {'name': center})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/center_user')


def check_mac(request, id):
    if 'center' in request.session:
        center = Requests_Client.objects.get(id=id)
        mac = center.mac
        user = Client_Request.objects.get(user_email=center.email)
        temporary_mac = user.mac
        client = Client_Details.objects.get(email=center.client_details.email)
        original_mac = client.mac
        name = Company_Details.objects.get(email=center.email)
        key = File_Details.objects.get(file=center.user_file)
        secure_key = key.secure_key
        print(secure_key)
        if original_mac == mac:
            center.same = True
            center.save()
            key.download = True
            key.finish = False
            key.save()
            subject = 'It is very Secure'
            message = f'Key Generate,... {secure_key}, Do not share any one'
            from_email = 'virualmachine123@gmail.com'
            to_email = [client.email]
            print(to_email)
            res = send_mail(subject, message, from_email, to_email)
            if res == 1:
                messages.info(request, 'Mail send Successfully')
            else:
                messages.info(request, 'Sorry,could not send mail')
            messages.success(request, 'Mac Address is Same')
        elif temporary_mac == mac:
            center.temporary_mac = True
            center.save()
            key.answer = False
            key.finish = True
            name.save()
            subject = 'It is very Secure'
            message = f'Key Generate,... {secure_key}, Do not share any one'
            from_email = 'virualmachine123@gmail.com'
            to_email = [client.email]
            res = send_mail(subject, message, from_email, to_email)
            if res == 1:
                messages.info(request, 'Mail send Successfully')
            else:
                messages.info(request, 'Sorry,could not send mail')
            messages.success(request, 'Send Question Link')
        else:
            center.different = True
            center.save()
            messages.success(request, 'Different physical address')
        return redirect(f'/view_client_request/{name.id}')
    else:
        messages.success(request, 'Session Expired')
        return redirect('/center_user')


def send_to_organization(request, id):
    if 'center' in request.session:
        client = Requests_Client.objects.get(id=id)
        new = Client_Details.objects.get(email=client.client_details.email)
        change = Change_Mac()
        change.client = new
        change.email = client.email
        change.different_mac = True
        change.file_name = client.file_name
        change.files = client.user_file
        change.client_email = new.email
        change.save()
        client.sent_organization = True
        client.save()
        messages.success(request, 'Sent Organization successfully')
        return redirect('/view_director_accept')
    else:
        messages.success(request, 'Session Expired')
        return redirect('/center_login')
