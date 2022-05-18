from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from user.models import *
from center.models import *
from django.core.mail import send_mail


# Create your views here.


def home(request):
    return render(request, 'main/home.html')


def director_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            users = Director.objects.get(email=email)
            if users.password == password:
                request.session['director'] = users.email
                messages.success(request, 'Login Successfully')
                return redirect('/director_user')
            else:
                messages.success(request, 'password is wrong')
                return redirect('/director_login')
        except Director.DoesNotExist:
            messages.success(request, 'Email id does not exist')
            return redirect('/director_login')
    return render(request, 'director/login.html')


def director_user(request):
    if 'director' in request.session:
        return render(request, 'director/director_user.html')
    else:
        return redirect('/director_login')


def director_logout(request):
    request.session.pop('director', None)
    messages.success(request, 'Logout Successfully')
    return redirect('/')


def company_details_views(request):
    if 'director' in request.session:
        user = Company_Details.objects.all()
        messages.success(request, 'User company details')
        return render(request, 'director/view_company.html', {'name': user})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/director_login')


def director_approve(request, id):
    if 'director' in request.session:
        user = Company_Details.objects.get(id=id)
        user.approve = True
        user.save()
        messages.success(request, 'Approve Successfully')
        return redirect('/company_details_views')
    else:
        messages.success(request, 'Session Expired')
        return redirect('/director_login')


def director_decline(request, id):
    if 'director' in request.session:
        user = Company_Details.objects.get(id=id)
        user.decline = True
        user.save()
        messages.success(request, 'Decline Successfully')
        return redirect('/company_details_views')
    else:
        messages.success(request, 'Session Expired')
        return redirect('/director_login')


def view_acceptance(request):
    if 'director' in request.session:
        user = Company_Details.objects.filter(approve=True)
        messages.success(request, 'Acceptance Users')
        return render(request, 'director/view_acceptance.html', {'name': user})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/director_login')


def view_format(request, id):
    if 'director' in request.session:
        user = Company_Details.objects.get(id=id)
        formats = File_Details.objects.filter(email=user.email)
        messages.success(request, f'{user.name} is file format')
        return render(request, 'director/view_format.html', {'name': formats})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/director_login')


def upload_price(request, id):
    if 'director' in request.session:
        user = File_Details.objects.get(id=id)
        if request.method == 'POST':
            user.file_amount = request.POST.get('price_amount')
            user.fix_amount = True
            user.save()
            messages.success(request, 'Price Upload Successfully')
            return redirect('/view_acceptance')
        return render(request, 'director/fix_amount.html', {'name': user.id})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/director_login')


def send_center(request, id):
    if 'director' in request.session:
        user = File_Details.objects.get(id=id)
        user.send_data = True
        user.save()
        messages.success(request, 'Send Data Center Successfully')
        return redirect('/view_acceptance')
    else:
        messages.success(request, 'Session Expired')
        return redirect('/director_login')


###################

def view_temporary_physical(request):
    if 'director' in request.session:
        user = Company_Details.objects.filter(approve=True)
        messages.success(request, 'Approve users')
        return render(request, 'director/view_temporary_physical.html', {'name': user})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/director_login')


def view_approve_client(request, id):
    if 'director' in request.session:
        user = Company_Details.objects.get(id=id)
        client = Change_Mac.objects.filter(email=user.email, approve=True)
        messages.success(request, 'User approve client')
        return render(request, 'director/view_approve_client.html', {'name': client})
    else:
        messages.success(request, 'Session Expired')
        return redirect('/director_login')


def send_secure_key(request, id):
    if 'director' in request.session:
        client = Change_Mac.objects.get(id=id)
        user = File_Details.objects.get(file=client.files)
        secure_key = user.secure_key
        print(secure_key)
        subject = 'It is very Secure'
        message = f'Key Generate,... {secure_key}, Do not share any one'
        from_email = 'virualmachine123@gmail.com'
        to_email = [client.email]
        print(to_email)
        res = send_mail(subject, message, from_email, to_email)
        if res == 1:
            client.director_sent = True
            client.security = secure_key
            client.save()
            messages.info(request, 'Mail send Successfully')
            return redirect('/view_temporary_physical')
        else:
            messages.info(request, 'Sorry,could not send mail')
            return redirect('/view_temporary_physical')
    else:
        messages.success(request, 'Session Expired')
        return redirect('/director_login')
