from django.contrib.auth.forms import UserCreationForm

from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import EmailForm, UserProfileForm, RegistrationForm, CustomUserCreationForm
from .models import Email, UserProfile
from .serializers import EmailSerializer
from .tasks import send_email_task, add, hello
from mailApp import throttles


def send_email_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.save(commit=False)  # Don't save to DB yet
            email.sender = request.user.email  # Set sender to current user's email
            email.save()  # Save to DB
            send_email_task.delay(email.id)  # Queue task
            return HttpResponse("Email is being sent in the background.")
    else:
        form = EmailForm()
    return render(request, 'tasks/send_email.html', {'form': form})

@api_view(['GET', 'POST'])
@throttle_classes([throttles.RoleBasedThrottle])
def email_list(request):
    if request.method == 'GET':
        emails = Email.objects.all()
        serializer = EmailSerializer(emails, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
def email_detail(request, pk):
    city = get_object_or_404(Email, pk=pk)

    if request.method == 'GET':
        serializer = EmailSerializer(city)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EmailSerializer(city, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        city.delete()
        return Response({'message': 'Email deleted successfully'}, status=204)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, email=user.email, name = user.username)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


class ProfileView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = request.user.userprofile
        return Response({
            'name': user_profile.name,
            'email': user_profile.email,
            'description': user_profile.description,
            'age': user_profile.age,
            'telegram_account': user_profile.telegram_account
        })

    def put(self, request):
        user_profile = request.user.userprofile
        data = request.data

        # Update user profile fields
        user_profile.description = data.get('description', user_profile.description)
        user_profile.age = data.get('age', user_profile.age)
        user_profile.telegram_account = data.get('telegram_account', user_profile.telegram_account)

        # Save the profile changes
        user_profile.save()

        # Update username or email if provided
        request.user.username = data.get('name', request.user.username)
        request.user.email = data.get('email', request.user.email)
        request.user.save()

        return Response({
            'message': 'Profile updated successfully',
            'name': request.user.username,
            'email': request.user.email,
            'description': user_profile.description,
            'age': user_profile.age,
            'telegram_account': user_profile.telegram_account
        }, status=status.HTTP_200_OK)
# def create_user_profile(request):
#     if request.method == "POST":
#         form = UserProfileForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('success_page')
#     else:
#         form = UserProfileForm()
#
#     return render(request, 'user_profile_form.html', {'form': form})

