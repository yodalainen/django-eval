import base64
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
from django.http import HttpResponse

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Hardcoded check as requested
            if username == 'test' and password == 'test':
                # We need a user object to log in via Django's session system.
                # If the user doesn't exist, create it for this demo.
                user, created = User.objects.get_or_create(username=username)
                if created:
                    user.set_password(password)
                    user.save()
                
                # Use Django's authentication system to log the user in
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('welcome')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def welcome_view(request):
    if not request.user.is_authenticated:
        auth_param = request.GET.get('auth') == 'basic'
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if auth_param or auth_header:
            if auth_header:
                try:
                    auth_type, auth_string = auth_header.split(' ', 1)
                    if auth_type.lower() == 'basic':
                        decoded_auth = base64.b64decode(auth_string).decode('utf-8')
                        username, password = decoded_auth.split(':', 1)
                        
                        if username == 'test' and password == 'test':
                            user, created = User.objects.get_or_create(username=username)
                            if created:
                                user.set_password(password)
                                user.save()
                            
                            user = authenticate(request, username=username, password=password)
                            if user is not None:
                                login(request, user)
                            else:
                                # If password changed or something, update it
                                user.set_password(password)
                                user.save()
                                user = authenticate(request, username=username, password=password)
                                if user:
                                    login(request, user)
                        else:
                            response = HttpResponse("Unauthorized", status=401)
                            response['WWW-Authenticate'] = 'Basic realm="Welcome"'
                            return response
                except Exception:
                    pass

            if not request.user.is_authenticated:
                response = HttpResponse("Unauthorized", status=401)
                response['WWW-Authenticate'] = 'Basic realm="Welcome"'
                return response
        else:
            return redirect('login')
            
    return render(request, 'accounts/welcome.html')
