from django.http import HttpResponse

from django.contrib.auth import login as dj_login
from django.contrib.auth import logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.sites.models import RequestSite
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader

from account.crawl import get_profs
from account.forms import SignInForm, PasswordForm
from account.models import Member, Student
from base.utils import save_file


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('dashboard'))
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            next_url = request.GET.get('next')
            user = form.user
            dj_login(request, user)
            if not next_url:
                next_url = reverse('dashboard')
            return HttpResponseRedirect(next_url)
    else:
        form = SignInForm()
    return render(request, 'account/login.html', {
        'form': form,
    })


def logout(request):
    dj_logout(request)
    return redirect('login')


@login_required
def password_reset_change(request):
    if request.method == 'POST':
        form = PasswordForm(user=request.user, data=request.POST)
        form.is_valid()
        sent = True
    else:
        form = PasswordForm(user=request.user)
        sent = False
    return render(request,
                  'password_reset/password_change.html',
                  {
                      'form': form,
                      'sent': sent,
                  })


@login_required
def dashboard(request):
    return render(
        request,
        'dashboard.html',
        {

        })


@login_required
def get_professors(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    get_profs()
    return HttpResponse('success')


@login_required
def create_accounts(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    message = ""
    if request.method == "POST":
        emails_file = request.FILES.get('emails')
        if not emails_file:
            message = "file is required"
        else:
            emails_file = save_file(emails_file)
            file_lines = open(emails_file, 'r').readlines()
            for i in range(len(file_lines)):
                line = file_lines[i]
                splitted_line = line.split('-')
                try:
                    new_email = splitted_line[0].lower()
                except:
                    message += str(i)
                try:
                    new_std_id = splitted_line[1]
                except:
                    new_std_id = ""
                new_password = Member.objects.make_random_password(length=10)
                if '@' in new_email:
                    new_username = new_email[:new_email.find('@')]
                else:
                    new_username = new_email
                    new_email = new_username + "@ce.sharif.edu"
                try:
                    member = Member.objects.get(username=new_username)
                except:
                    try:
                        context = {
                            'site': RequestSite(request),
                            'username': new_username,
                            'password': new_password,
                            'secure': request.is_secure(),
                        }
                        subject = loader.render_to_string("account/email/new_account_email_subject.txt",
                                                          context).strip()
                        text_body = loader.render_to_string("account/email/new_account_email.txt",
                                                            context).strip()

                        msg = EmailMessage(subject=subject, from_email="shora.cesharif@gmail.com",
                                           to=[new_email], body=text_body)
                        msg.send()
                        new_member = Student.objects.create(username=new_username,
                                                            std_id=new_std_id,
                                                            email=new_email,
                                                            password=make_password(new_password))
                    except Exception as e:
                        print e
                        message += "%d\n" % i

            if message:
                message += "making account for this lines is not possible, please contact A\'min"
            else:
                message = "success"
    return render(request, 'account/create_account.html', {
        'message': message,
    })


