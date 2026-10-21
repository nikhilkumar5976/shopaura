from django.shortcuts import render, redirect
from django.contrib import auth, messages

from accounts.models import Account
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username=email.split('@')[0]

            user=Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number=phone_number
            user.save()
            messages.success(request, 'Your account has been successfully created.')
            return redirect('register')  # Redirect to the same page or any other page after successful registration

    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)

def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            # User is authenticated, you can log them in
            auth.login(request, user)
            #messages.success(request, 'You are now logged in.')
            return redirect('home')  # Redirect to the home page or any other page after successful login
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('signin')  # Redirect back to the login page on failure
    return render(request, 'accounts/signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('signin')  # Redirect to the login page after logout