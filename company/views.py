from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from user.models import *
from center.models import *
import re


# Create your views here.

def company_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            users = Company.objects.get(email=email)
            if users.password == password:
                request.session['company'] = users.email
                messages.success(request, 'Login Successfully')
                return redirect('/company_user')
            else:
                messages.success(request, 'password is wrong')
                return redirect('/company_login')
        except Company.DoesNotExist:
            messages.success(request, 'Email id does not exist')
            return redirect('/company_login')
    return render(request, 'company/login.html')


def company_register(request):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[gmail]+(\.[A-Z|a-z]{2,})+')
    if request.method == "POST":
        reg = Company()
        reg.name = request.POST.get('name')
        reg.email = request.POST.get('email')
        reg.password = request.POST.get('password')
        if re.fullmatch(regex, reg.email):
            try:
                main = Company.objects.get(email=reg.email)
                messages.success(request, 'Email-Id already exists')
                return redirect('/company_register')
            except:
                reg.save()
                messages.success(request, 'Register Successfully')
                return redirect('/company_login')
        else:
            messages.success(request, 'Invalid Email-Id')
            return redirect('/company_register')
    return render(request, 'company/register.html')


def company_user(request):
    if 'company' in request.session:
        return render(request, 'company/company_user.html')
    else:
        return redirect('/company_login')


def company_logout(request):
    request.session.pop('company', None)
    messages.success(request, 'Logout Successfully')
    return redirect('/')


def view_user_company(request):
    if 'company' in request.session:
        user = Company_Details.objects.filter(approve=True)
        messages.success(request, 'User company details')
        return render(request, 'company/view_user_company.html', {'name': user})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/company_login')


def view_partner_client(request, id):
    if 'company' in request.session:
        user = Company_Details.objects.get(id=id)
        client = Change_Mac.objects.filter(email=user.email)
        messages.success(request, 'Partner Client company')
        return render(request, 'company/view_partner_client.html', {'name': client})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/company_login')


def sent_question_link(request, id):
    if 'company' in request.session:
        client = Change_Mac.objects.get(id=id)
        client.question_link = True
        client.save()
        messages.success(request, "Question link sent")
        return redirect('/view_user_company')
    else:
        messages.success(request, 'Session Expired')
        return redirect('/company_login')


def check_now_mac(request, id):
    if 'company' in request.session:
        client = Change_Mac.objects.get(id=id)
        now_mac = client.current_mac
        req = Requests_Client.objects.get(client_email=client.client_email)
        print(req)
        old_mac = req.mac
        if now_mac == old_mac:
            client.sent_user = True
            client.save()
            return redirect('/view_user_company')
        else:
            client.again_link = True
            client.save()
            return redirect('/view_user_company')
    else:
        messages.success(request, 'Session Expired')
        return redirect('/company_login')
