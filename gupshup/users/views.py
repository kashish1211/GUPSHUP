from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ProfileRegisterForm
from verify_email.email_handler import send_verification_email
from django.contrib.auth import login


def register(request):
    if request.method == 'POST':
        form_u = UserRegisterForm(request.POST)
        # form_p = ProfileRegisterForm(request.POST, request.FILES)
        if form_u.is_valid():
            form_u.save()
            username = form_u.cleaned_data.get('username')
            inactive_user = send_verification_email(request, form_u)
            
            return redirect('verify')
            messages.success(request, f'Your account has been created! Please verify your email to log in!')
    else:
        form_u = UserRegisterForm()
        # form_p = ProfileRegisterForm()
    return render(request, 'users/register.html', {'form_u': form_u})

def verify(request):
    return render(request,'users/verify.html')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
       	p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
       	'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


def handler500(request, *args, **argv):
    return render(request, 'users/500.html', status=500)

def handler404(request, *args, **argv):
    return render(request, 'users/404.html', status=404)


def profilereg(request):
    
    
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        
        p_form = ProfileRegisterForm()
    context = {
       	'p_form': p_form
    }

    return render(request, 'users/profilereg.html', context)