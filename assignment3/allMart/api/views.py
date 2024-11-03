import logging

from django.contrib.sites import requests
from django.core.cache import cache
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from .models import KeyValue
from .serializers import KeyValueSerializer
from prometheus_client import Counter, generate_latest
from django.http import HttpResponse

class KeyValueStore:
    def __init__(self):
        self.instances = [
            'http://localhost:8000',
            'http://localhost:8001',
            'http://localhost:8002',
            'http://localhost:8003',
        ]
        self.write_quorum = 2
        self.read_quorum = 2

    def quorum_write(self, key, value):
        success_count = 0
        data = {'key': key, 'value': value, 'timestamp': timezone.now().isoformat()}
        for instance in self.instances:
            try:
                response = requests.post(f"{instance}/write/", json=data)
                if response.status_code == 200:
                    success_count += 1
                if success_count >= self.write_quorum:
                    return JsonResponse({"status": "success"})
            except requests.RequestException:
                continue
        return JsonResponse({"status": "failure", "error": "Write quorum not reached"})

    def quorum_read(self, key):
        responses = []
        for instance in self.instances:
            try:
                response = requests.get(f"{instance}/read/{key}/")
                if response.status_code == 200:
                    responses.append(response.json())
                if len(responses) >= self.read_quorum:
                    break
            except requests.RequestException:
                continue
        if len(responses) < self.read_quorum:
            return JsonResponse({"status": "failure", "error": "Read quorum not reached"})

        latest_value = max(responses, key=lambda x: x['timestamp'])
        return JsonResponse({"status": "success", "data": latest_value})

class KeyValueStoreView(APIView):
    def get(self, request, key=None):
        if key:
            # Check cache first
            cached_kv = cache.get(key)
            if cached_kv is not None:
                return Response(cached_kv, status=status.HTTP_200_OK)

            try:
                kv = KeyValue.objects.get(key=key)
                serializer = KeyValueSerializer(kv)
                cache.set(key, serializer.data, timeout=60*15)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except KeyValue.DoesNotExist:
                return Response({'error': 'Key not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            kv_pairs = KeyValue.objects.all()
            serializer = KeyValueSerializer(kv_pairs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = KeyValueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete_many([])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, key):
        try:
            kv = KeyValue.objects.get(key=key)
            serializer = KeyValueSerializer(kv, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                cache.set(key, serializer.data, timeout=60*15)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KeyValue.DoesNotExist:
            return Response({'error': 'Key not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, key):
        try:
            kv = KeyValue.objects.get(key=key)
            kv.delete()
            cache.delete(key)
            return Response({'message': 'Key deleted'}, status=status.HTTP_204_NO_CONTENT)
        except KeyValue.DoesNotExist:
            return Response({'error': 'Key not found'}, status=status.HTTP_404_NOT_FOUND)
# @csrf_exempt
# def write_view(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         key = data['key']
#         value = data['value']
#         timestamp = parse_datetime(data['timestamp'])
#         KeyValue.objects.update_or_create(key=key, defaults={'value': value, 'timestamp': timestamp})
#         return JsonResponse({"status": "success"})
#     return JsonResponse({"status": "failure", "error": "Invalid request"})
#
# def read_view(request, key):
#     try:
#         kv = KeyValue.objects.get(key=key)
#         return JsonResponse({
#             "key": kv.key,
#             "value": kv.value,
#             "timestamp": kv.timestamp.isoformat(),
#         })
#     except KeyValue.DoesNotExist:
#         return JsonResponse({"status": "failure", "error": "Key not found"})
#

logger = logging.getLogger(__name__)

def test_logging(request):
    logger.debug('This is a debug message.')
    logger.info('This is an info message.')
    logger.warning('This is a warning message.')
    logger.error('This is an error message.')
    logger.critical('This is a critical message.')
    return HttpResponse('Logging tested, check the console and log file!')

