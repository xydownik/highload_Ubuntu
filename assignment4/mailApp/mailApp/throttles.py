from rest_framework.throttling import  UserRateThrottle
from django.core.cache import cache
from django.contrib.auth.models import User


class RoleBasedThrottle(UserRateThrottle):
    def get_cache_key(self, request, view):
        # Identify user role
        if request.user.is_authenticated:
            if request.user.is_staff:  # Treat staff as "admin"
                self.scope = 'admin'
            else:
                self.scope = 'user'
        else:
            self.scope = 'anon'  # For anonymous users

        # Generate a cache key based on the scope and user identity
        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request),
        }
