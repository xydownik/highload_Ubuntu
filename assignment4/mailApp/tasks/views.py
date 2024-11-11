from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .forms import EmailForm
from .models import Email
from .serializers import EmailSerializer
from .tasks import send_email_task, add


def index(request):
    # Trigger asynchronous tasks
    add.delay(4, 4)
    send_email_task.delay(
        subject='Hello',
        message='This is a test email.',
        recipient_list=['user@gmail.com']
    )
    return HttpResponse("Tasks are being processed!")


def send_email_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.save()  # Save email to DB
            send_email_task.delay(email.id)  # Queue task
            return HttpResponse("Email is being sent in the background.")
    else:
        form = EmailForm()
    return render(request, 'tasks/send_email.html', {'form': form})

@api_view(['GET', 'POST'])
def email_list(request):
    if request.method == 'GET':
        cities = Email.objects.all()
        serializer = EmailSerializer(cities, many=True)
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
