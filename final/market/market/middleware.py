# middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

class SecureHeadersMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response['X-Content-Type-Options'] = 'nosniff'
        response['Content-Security-Policy'] = "default-src 'self'"
        return response
