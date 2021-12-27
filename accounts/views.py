import os

from django.conf import settings as django_settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib.auth.password_validation import validate_password, password_validators_help_text_html
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .models import Company
from .models import ExtendedUsers
from .tokens import account_activation_token


@login_required(redirect_field_name=None)
def account_settings(request):
    context = {'sub_template': 'account-change-password'}
    return render(request, 'account_settings.html', context)


@login_required(redirect_field_name=None)
def company_details(request):
    company = Company.objects.filter(comp_name=request.user.extendedusers.comp_name)
    return render(request, 'company_details.html', {'company': company})


@login_required(redirect_field_name=None)
def connections(request):
    if request.method == 'POST':
        comp_name = request.POST['comp_name']
        if not Company.objects.filter(comp_name=comp_name).exists():
            newextendeduser = ExtendedUsers.objects.filter(user=request.user)
            company = Company(comp_name=comp_name, emp_id=request.user, emp_position='Owner', verify=True)
            newextendeduser.update(own_comp=True, comp_name=comp_name)
            company.save()

            messages.success(request, 'Your company registered successfully...')
        else:
            messages.info(request,
                          'company name is already exists... please change your company name or join your organization')
        return render(request, 'account_settings.html')
    return render(request, 'account_settings.html')


@login_required(redirect_field_name=None)
def editprofile(request):
    if request.method == 'POST' and 'editsaveprofile' in request.POST:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        p_desc = request.POST['p_desc']
        # user_info = User.objects.get(request.POST)
        # user = User.objects.update(user_info, first_name=first_name, last_name=last_name
        #                            , email=email)
        newextendeduser = ExtendedUsers.objects.filter(user=request.user)
        print(request.user)
        newextendeduser.update(p_desc=p_desc)
        # newextendeduser.save()
        user_info = User.objects.get(username=request.user.username)
        user_info.first_name = first_name
        user_info.last_name = last_name
        user_info.email = email
        # user_info.extendedusers.p_desc = p_desc
        user_info.save()
        print('edited successfully...')
        return render(request, 'account_settings.html')

    if request.method == 'POST' and 'upload_p_pic' in request.POST:
        user = User.objects.get(username=request.user.username)
        content = request.FILES['p_pic'].read()
        # print(content)
        file = open(os.path.join(django_settings.STATICFILES_DIRS[0], f'{user.username}.jpg'), 'wb+')
        file.write(content)
        print(file)
        file.close()
        print(file.name)
        print(f'{user.username}.jpg')
        newextendeduser = ExtendedUsers.objects.filter(user=request.user)
        newextendeduser.update(p_pic=f'{user.username}.jpg')

    # if user is not authenticated redirect to home page
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return render(request, 'home.html')

    return render(request, 'account_settings.html')


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.get(username=username)
        if user.is_active:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                print(user)
                if request.POST.get('remember_me', None):
                    print('run')
                    request.session.set_expiry(60 * 60 * 24 * 28)  # session expires in a month
                return redirect('/')
            else:
                messages.info(request, 'Invalid Credentials! Remember Credentials are Case Sensitive!')
                return redirect('login')
        else:
            messages.info(request, 'your email id is not verified! please click on the link sent on your email id')
            return redirect('login')
    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        c_password = request.POST['c_password']
        try:
            validate_email(email)
            if password == c_password:
                try:
                    validate_password(password)
                    if User.objects.filter(username=username).exists():
                        messages.info(request, "username already exists, try to choose other username!")
                        return redirect('register')

                    elif User.objects.filter(email=email).exists():
                        messages.info(request, "email already taken, please enter carefully!")
                        return redirect('register')

                    else:
                        user = User.objects.create_user(username=username, password=password, email=email,
                                                        first_name=first_name,
                                                        last_name=last_name)
                        newextendeduser = ExtendedUsers(p_pic='', p_desc='', own_comp=False, user=user)
                        user.is_active = False
                        user.save()
                        newextendeduser.save()
                        current_site = get_current_site(request)
                        mail_subject = 'Activate your account.'
                        message = render_to_string('verify_email.html', {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                        })
                        to_email = email
                        email = EmailMessage(
                            mail_subject, message, to=[to_email]
                        )
                        email.send()
                        messages.info(request, 'user created successfully!!!')
                    return redirect('email_sent')
                except ValidationError:
                    messages.info(request, password_validators_help_text_html())
                    return render(request, 'register.html')
            else:
                messages.info(request, 'password mismatch')
                return redirect('register')
        except ValidationError:
            messages.info(request, "email address is incorrect")
            return redirect('register')
    else:
        return render(request, 'register.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse(
            'Activation link is invalid!This will happen if you are accessing this link again or it will expired!')


def email_sent(request):
    return render(request, 'email_sent.html')


@login_required(redirect_field_name=None)
def delete_user(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.user.username)
            user.delete()
            messages.success(request, "The user is deleted...")
            messages.success(request, "Signing Out! ")
            messages.success(request, "redirecting to Login Page... ")
            return render(request, 'login.html')
        except User.DoesNotExist:
            messages.error(request, "User does not exist")
            return render(request, 'account_settings.html')
        except Exception as e:
            messages.error(request, "Error Deleting user")
            return render(request, 'account_settings.html')
    return render(request, 'account_settings.html')


@login_required(redirect_field_name=None)
def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required(redirect_field_name=None)
def change_password(request):
    if request.method == 'POST':
        if request.user.check_password(request.POST['c_pass']):
            if request.POST['n_pass'] == request.POST['r_pass']:
                try:
                    validate_password(request.POST['n_pass'])
                    user = User.objects.get(username=request.user.username)
                    user.set_password(request.POST['n_pass'])
                    user.save()
                    messages.success(request, 'Password Changed Successfully! login again...')
                    print('success')
                    return render(request, 'login.html')
                except ValidationError:
                    messages.info(request, password_validators_help_text_html())
                    return render(request, 'account_settings.html')
            else:
                messages.info(request, 'new password and repeat password are not same')
                return render(request, 'account_settings.html')
        else:
            messages.info(request, 'current password field is invalid')
            return render(request, 'account_settings.html')
    return render(request, 'account_settings.html')


def verify_account(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            if user.is_active:
                messages.info(request,
                              'Account already active do not need to verify it. you can simply login to your account!')
                redirect('verify_account')
            else:
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('verify_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                messages.info(request, 'Email sent successfully!!!')
        except:
            messages.info(request, 'Email not found! please check your field.')
    return render(request, 'verify_account.html')
