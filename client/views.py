import base64
import requests
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import re, uuid
from user.models import *
from center.models import *
from . import encrypt
from django.conf import settings
import random
import re


# Create your views here.


def client_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            users = Client.objects.get(email=email)
            if users.password == password:
                request.session['client'] = users.email
                messages.success(request, 'Login Successfully')
                return redirect('/client_user')
            else:
                messages.success(request, 'password is wrong')
                return redirect('/client_login')
        except Client.DoesNotExist:
            messages.success(request, 'Email id does not exist')
            return redirect('/client_login')
    return render(request, 'client/login.html')


def client_register(request):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[gmail]+(\.[A-Z|a-z]{2,})+')
    if request.method == "POST":
        reg = Client()
        reg.name = request.POST.get('name')
        reg.email = request.POST.get('email')
        reg.password = request.POST.get('password')
        if re.fullmatch(regex, reg.email):
            try:
                main = Client.objects.get(email=reg.email)
                messages.success(request, 'Email id Already Exits')
                return redirect('/client_register')
            except:
                reg.save()
                messages.success(request, 'Register Successfully')
                return redirect('/client_login')
        else:
            messages.success(request, 'Invalid Email-Id')
            return redirect('/client_register')
    return render(request, 'client/register.html')


def client_user(request):
    if 'client' in request.session:
        return render(request, 'client/client_user.html')
    else:
        return redirect('/client_login')


def client_logout(request):
    request.session.pop('client', None)
    messages.success(request, 'Logout Successfully')
    return redirect('/')


def client_company(request):
    if 'client' in request.session:
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[gmail]+(\.[A-Z|a-z]{2,})+')
        name = Client.objects.get(email=request.session['client'])
        if request.method == "POST":
            upload = Client_Details()
            upload.company_name = request.POST.get('company_name')
            upload.email = name.email
            upload.address = request.POST.get('address')
            upload.name = name.name
            upload.mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
            upload.company_email = request.POST.get('company_email')
            upload.contact = request.POST['mobile']
            if re.fullmatch(regex, upload.company_email):
                try:
                    client = Client_Details.objects.get(company_email=upload.company_email)
                    messages.success(request, 'Emil-Id already exits')
                    return redirect('/client_company')
                except:
                    upload.save()
                    messages.success(request, 'Company Details Upload Successfully')
                    return redirect('/client_user')
            else:
                messages.success(request, 'Invalid Email-Id')
                return redirect('/client_company')
        return render(request, 'client/client_company.html',
                      {'email': name.email, 'name': name.name})

    else:
        messages.success(request, 'Session Expired')
        return redirect('/client_login')


def search_files(request):
    if 'client' in request.session:
        if request.method == 'POST':
            search_term = request.POST.get('search')
            try:
                name = Company_Details.objects.all().filter(company_name__icontains=search_term)[0]
                company = name.company_name
                return render(request, 'client/search_files.html', {'name': search_term, 'company': company, 'i': name})
            except:
                return render(request, 'client/search_files.html', {'name': search_term, 'company': None, 'i': None})
        return render(request, 'client/search_files.html')
    else:
        messages.success(request, 'Session Expired')
        return redirect('/client_login')


def client_request(request, id):
    if 'client' in request.session:
        name = Company_Details.objects.get(id=id)
        client = Client_Details.objects.get(email=request.session['client'])
        try:
            user = Client_Request.objects.get(company_name=client.company_name, email=client.email)
            messages.success(request, 'You have already Request Send')
        except:
            user = Client_Request()
            user.name = client.name
            user.company_name = client.company_name
            user.email = client.email
            user.contact = client.contact
            user.address = client.address
            user.company_email = client.company_email
            user.mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
            user.user_email = name.email
            user.partner = name
            user.save()
            messages.success(request, 'Request Send Successfully')
        return redirect('/search_files')
    else:
        messages.success(request, 'Session Expired')
        return redirect('/client_login')


def user_link(request):
    if 'client' in request.session:
        client = Client_Details.objects.get(email=request.session['client'])
        user = Client_Request.objects.filter(email=client.email, accept=True)
        messages.success(request, 'Acceptance User')
        return render(request, 'client/user_link.html', {'name': user})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/client_login')


def question_answer(request, id):
    if 'client' in request.session:
        client = Client_Details.objects.get(email=request.session['client'])
        war = Client_Request.objects.get(id=id)
        email = war.user_email
        try:
            name = Question.objects.get(email=email)
            if request.method == 'POST':
                one = request.POST.get('one')
                two = request.POST.get('two')
                three = request.POST.get('three')
                four = request.POST.get('four')
                five = request.POST.get('five')
                if one == name.one:
                    if two == name.two:
                        if three == name.three:
                            if four == name.four:
                                if five == name.five:
                                    war.answer = True
                                    war.save()
                                    messages.success(request, 'Answer is Correct')
                                    return redirect('/user_link')
                                else:
                                    messages.success(request, 'Try Again')
                            else:
                                messages.success(request, 'Try Again')
                        else:
                            messages.success(request, 'Try Again')
                    else:
                        messages.success(request, 'Try Again')
                else:
                    messages.success(request, 'Try Again')
        except:
            messages.success(request, 'User Is not set Question')
            return redirect('/user_link')
        return render(request, 'client/question_answer.html', {'name': client, 'id': war.id})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/client_login')


def client_view_files(request, id):
    if 'client' in request.session:
        name = Client_Request.objects.get(id=id)
        user = File_Details.objects.filter(email=name.user_email)
        messages.success(request, 'View user files')
        return render(request, 'client/client_view_files.html', {'data': user, 'a': name.id, 'b': name})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/client_login')


def file_request(request, id):
    if 'client' in request.session:
        user = File_Details.objects.get(id=id)
        client = Client_Details.objects.get(email=request.session['client'])
        center = Requests_Client()
        center.client_details = client
        center.email = user.email
        center.user_file = user.file
        center.file_name = user.file_name
        center.client_email = request.session['client']
        center.mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        center.save()
        user.finish = True
        user.save()
        messages.success(request, 'Files Request Send Successfully')
        return redirect('/user_link')
    else:
        messages.success(request, 'Session Expired')
        return redirect('/client_login')


def file_download(request, id):
    user = File_Details.objects.get(id=id)
    file = user.file
    generator_key = user.secure_key
    client = Client_Details.objects.get(email=request.session['client'])
    if request.method == 'POST':
        print(1)
        key = request.POST.get('keys')
        keys = key.encode()
        keys = base64.b64encode(keys)
        if key == generator_key:
            response = encrypt.decrypt_file(f'{settings.MEDIA_ROOT}/{file}', keys)
            messages.success(request, 'File Download')
            return response
        else:
            messages.success(request, 'Please File Correct Key')
            return redirect('/user_link')
    return render(request, 'client/file_download.html',
                  {'name': client.name, 'n_email': client.email, 'project': user.file_name, 'location': client.address,
                   'phone': client.contact, 'company_email': client.company_email, 'id': user.id})


def different_physical(request):
    if 'client' in request.session:
        change = Change_Mac.objects.filter(client_email=request.session['client'])
        messages.success(request, 'Different physical address link')
        return render(request, 'client/different_physical.html', {'name': change})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/client_login')


def view_gk_question(request, id):
    if 'client' in request.session:
        mac = Change_Mac.objects.get(id=id)
        global a
        global gk
        gk = {'Name the Father of the Indian Constitution?': 'Dr. B. R. Ambedkar',
              'Who was the first Prime Minister of India?': 'Jawaharlal Nehru',
              'Who was the first woman Prime Minister of India?': ' Indira Gandhi',
              'Name the deepest ocean in the world?': 'Pacific Ocean',
              'Name the gas which is filled in balloons?': 'Helium',
              'Aizawl is the capital of which state of India?': 'Mizoram',
              'Bucharest is the capital of which country?': 'Romania',
              'The deepest part of the ocean is called?': 'Challenger Deep',
              '........... is the capital of Andhra Pradesh.': 'Amaravati',
              'Baby of a horse is known as.........': 'Foal', ' Young one of a cow is known as .......': 'Calf'}
        a = random.choices(list(gk.keys()), k=5)
        messages.success(request, 'Qk Question')
        return render(request, 'client/view_gk_question.html',
                      {'one': a[0], 'two': a[1], 'three': a[2], 'four': a[3], 'five': a[4], 'id': mac.id})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/client_login')


def check_answer(request, id):
    if 'client' in request.session:
        mac = Change_Mac.objects.get(id=id)
        global a
        global gk
        if request.method == 'POST':
            one = request.POST['one']
            two = request.POST['two']
            three = request.POST['three']
            four = request.POST['four']
            five = request.POST['five']
            if one == gk[a[0]]:
                if two == gk[a[1]]:
                    if three == gk[a[2]]:
                        if four == gk[a[3]]:
                            if five == gk[a[4]]:
                                mac.correct = True
                                mac.current_mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
                                mac.save()
                                return redirect('/different_physical')
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            else:
                messages.success(request, 'Try Again')
                return redirect(f'/view_gk_question/{mac.id}')
    else:
        messages.success(request, 'Session Expired')
        return redirect('/client_login')


def download(request, id):
    user = Change_Mac.objects.get(id=id)
    file = user.files
    print(file)
    generator_key = user.security
    client = Client_Details.objects.get(email=request.session['client'])
    if request.method == 'POST':
        print(1)
        key = request.POST.get('keys')
        keys = key.encode()
        keys = base64.b64encode(keys)
        if key == generator_key:
            response = encrypt.decrypt_file(f'{settings.MEDIA_ROOT}/{file}', keys)
            messages.success(request, 'File Download')
            return response
        else:
            messages.success(request, 'Please File Correct Key')
            return redirect('/user_link')
    return render(request, 'client/download.html',
                  {'name': client.name, 'n_email': client.email, 'project': user.file_name, 'location': client.address,
                   'phone': client.contact, 'company_email': client.company_email, 'id': user.id})
