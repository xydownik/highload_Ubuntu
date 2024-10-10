
from django.http import HttpResponse


class RoundRobinMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request (before the view is called)
        response = self.get_response(request)

        # Ensure response is not None
        if response is None:
            return HttpResponse("Empty Response", status=500)

        return response