from audioop import reverse

from django.contrib.auth import login as dj_login

from django.contrib.auth import logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from account.forms import SignInForm, PasswordForm



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
    return redirect('home')


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


def dashboard(request):
    return