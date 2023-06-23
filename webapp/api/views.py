from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from .forms import SignupForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import AccessToken

# {"username": "super",
# "password":"test",
# "user_type":super_admin,
# }


# Create your views here.
@api_view(['POST'])
def signup(request):
    # form = SignupForm(request.POST)
    # if form.is_valid():
    #         user = form.save(commit=False)
    #         user.set_password(form.cleaned_data['password'])
    #         user.save()
    #         messages.success(request, 'Registration successful. Please log in.')
    #         return redirect('login')
    username = request.data.get('username')
    password = request.data.get('password')
    user_type = request.data.get('user_type')

    if not username or not password or not user_type:
        return Response({'error' : 'Please provide all details'})
    
    try:
        user = CustomUser.objects.create_user(username=username, password=password)
        if user_type == 'super_admin':
            group = user.groups.add(SuperAdmin.objects.first())
        elif user_type == 'teacher':
            group = user.groups.add(Teacher.objects.first())
        elif user_type == 'student':
            group =user.groups.add(Student.objects.first())
        else:
            return Response({'error': 'Invalid user type.'}, status=status.HTTP_400_BAD_REQUEST)
        user.groups.add(group)

    except Exception as e:
        return Response({'error' : str(e)}, status=status.HTTP_400_BAD_REQUEST)
    # return render(request, 'api/signup.html', )
    return Response({'success': 'User created successfully.'}, { 'tokens': generate_tokens(user)}, status=status.HTTP_201_CREATED)


# @api_view(['GET'])              
# def login(request):
#     pass
def login(request):
	if request.method == 'POST':

		# AuthenticationForm_can_also_be_used__

		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username = username, password = password)
		if user is not None:
			form = login(request, user)
			messages.success(request, f' welcome {username} !!')
			return redirect('index')
		else:
			messages.info(request, f'account done not exit plz sign in')
	form = AuthenticationForm()
	return render(request, 'login.html', {'form':form, 'title':'log in'})

def index(request):
	return render(request, 'api/index.html', {'title':'index'})

@api_view(['POST'])
def forgot_password(request):
    email = request.data.get('email')
    user = get_object_or_404(CustomUser, email=email)
    
    # Generate password reset token
    token = default_token_generator.make_token(user)
    
    # Create password reset link
    reset_url = request.build_absolute_uri(reverse('reset_password', kwargs={'uidb64': user.pk, 'token': token}))
    
    # Send email to the user
    subject = 'Password Reset Request'
    message = f'Dear {user.username},\n\nPlease click the link below to reset your password:\n\n{reset_url}'
    from_email = 'noreply@your-website.com'
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)
    
    # Generate new JWT access token and return it as response
    access_token = AccessToken.for_user(user)
    response_data = {
        'access_token': str(access_token),
        'message': 'An email has been sent with instructions to reset your password.'
    }
    
    return Response(status=status.HTTP_200_OK, data=response_data)


def generate_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }