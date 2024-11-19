import os

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm

from django.http import HttpResponse, JsonResponse
# Create your views here.
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, permissions
from rest_framework.decorators import api_view, throttle_classes, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import EmailForm, UserProfileForm, RegistrationForm, CustomUserCreationForm
from .models import Email, UserProfile
from .serializers import EmailSerializer
from .tasks import send_email_task, add, hello
from mailApp.throttles import RoleBasedThrottle

from mailApp import settings


def send_email_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.save(commit=False)
            email.sender = request.user.email
            email.sent = True
            email.save()
            send_email_task.delay(email.id)
            return HttpResponse("Email is being sent in the background.")
    else:
        form = EmailForm()
    return render(request, 'tasks/send_email.html', {'form': form})

@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
@throttle_classes([RoleBasedThrottle])
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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = request.user.userprofile
        return Response({
            'name': user_profile.name,
            'email': user_profile.email,
            'description': user_profile.description,
            'age': user_profile.age,
            'telegram_account': user_profile.telegram_account,
            'UIN': user_profile.UIN
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

class UserEmailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        emails = Email.objects.filter(recipient=request.user.email)
        serializer = EmailSerializer(emails, many=True)
        return Response(serializer.data)


def logout_view(request):
    # permission_classes = [IsAuthenticated]
    logout(request)
    return redirect('login')

@csrf_exempt
def upload_file(request):
    if request.method == "POST" and "file" in request.FILES:
        file = request.FILES["file"]
        total_size = file.size
        uploaded_size = 0

        # Define a location to save the uploaded file
        upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
        os.makedirs(upload_dir, exist_ok=True)  # Ensure the directory exists
        file_path = os.path.join(upload_dir, file.name)

        # Save the file in chunks while tracking progress
        try:
            with open(file_path, "wb") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
                    uploaded_size += len(chunk)

                    # Calculate and send progress
                    progress = int((uploaded_size / total_size) * 100)
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        f"user_{request.user.id}_progress",
                        {"type": "send_progress", "progress": progress},
                    )
        except Exception as e:
            return JsonResponse({"error": f"File upload failed: {str(e)}"}, status=500)

        # Return success response after completing the upload
        return JsonResponse({"message": "Upload complete", "file_path": file_path})

    return JsonResponse({"error": "Invalid request. Please send a file via POST."}, status=400)

