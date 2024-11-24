from rest_framework.throttling import  UserRateThrottle


class RoleBasedThrottle(UserRateThrottle):
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_staff:
                self.scope = 'admin'
            else:
                self.scope = 'user'
        else:
            self.scope = 'anon'

        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(request),
        }
