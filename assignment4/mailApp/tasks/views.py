import os
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import EmailForm, CustomUserCreationForm, FileUploadForm
from .models import Email, UserProfile, UploadedFile
from .serializers import EmailSerializer
from .tasks import send_email_task,process_file
from mailApp.throttles import RoleBasedThrottle
import logging
import subprocess
#Create your views here.

logger = logging.getLogger(__name__)
@login_required(login_url='login')
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
    logger.debug('Fetching email list...')
    cached_emails = cache.get('email_list')
    if cached_emails:
        logger.debug('Email list fetched from cache.')
        return Response(cached_emails)

    if request.method == 'GET':
        emails = Email.objects.select_related('userprofile').all()
        serializer = EmailSerializer(emails, many=True)
        cache.set('email_list', serializer.data, timeout=300)
        logger.debug(f'Email list cached with {len(emails)} items.')
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info('New email created successfully.')
            return Response(serializer.data, status=201)
        logger.error(f'Error creating email: {serializer.errors}')
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
        cache_key = f"user_profile_{request.user.id}"
        cached_profile = cache.get(cache_key)

        if cached_profile:
            logger.debug(f"Profile data served from cache for user {request.user.id}.")
            return Response(cached_profile)

        user_profile = request.user.userprofile
        data = {
            'name': user_profile.name,
            'email': user_profile.email,
            'description': user_profile.description,
            'age': user_profile.age,
            'telegram_account': user_profile.telegram_account,
            'UIN': user_profile.UIN,
        }

        cache.set(cache_key, data, timeout=600)
        logger.debug(f"Profile data cached for user {request.user.id}.")
        return Response(data)

    def put(self, request):
        user_profile = request.user.userprofile
        data = request.data

        user_profile.description = data.get('description', user_profile.description)
        user_profile.age = data.get('age', user_profile.age)
        user_profile.telegram_account = data.get('telegram_account', user_profile.telegram_account)

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
    def get(self, request, id=None):
        if id is None:
            # List all emails for the authenticated user
            emails = Email.objects.filter(recipient=request.user.email)
            serializer = EmailSerializer(emails, many=True)
            return Response(serializer.data)
        else:
            # Retrieve a specific email by ID for the authenticated user
            email = Email.objects.filter(id=id, recipient=request.user.email).first()
            if not email:
                return Response(
                    {'error': 'Email not found or you do not have permission to view it.'},
                    status=404
                )
            serializer = EmailSerializer(email)
            return Response(serializer.data)

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def upload_file_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.user = request.user

            validate_file_type(uploaded_file)
            validate_and_save_file(uploaded_file)

            process_file.delay(uploaded_file.id)
            return redirect('upload_success')
        else:
            logger.error('File upload failed. Form invalid.')
    else:
        form = FileUploadForm()

    return render(request, 'tasks/upload.html', {'form': form})


def upload_success_view(request):
    return render(request, 'tasks/upload_success.html')

def file_progress_view(request, file_id):
    uploaded_file = UploadedFile.objects.get(id=file_id, user=request.user)
    return JsonResponse({
        'progress': uploaded_file.progress,
        'processed': uploaded_file.processed,
    })

def scan_file(file_path):
    try:
        result = subprocess.run(
            ["clamscan", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        logger.info(f"ClamAV scan result: {result.stdout}")
        if "FOUND" in result.stdout:
            raise ValidationError("The uploaded file contains malware.")
    except Exception as e:
        logger.error(f"Error during file scanning: {str(e)}")
        raise


def validate_and_save_file(uploaded_file):
    file_path = uploaded_file.file.path
    try:
        scan_file(file_path)
    except ValidationError:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise
def validate_file_type(uploaded_file):
    valid_extensions = ['csv']
    extension = uploaded_file.file.name.split('.')[-1].lower()
    if extension not in valid_extensions:
        raise ValidationError("Unsupported file format. Please upload a .csv file.")
