from django.conf import settings
from company.models import TblVendor
from django.core.cache import cache

'''
Used for the purpose of Login.
The following class needs to be mentioned in the settings file
'''
class AuthBackend:
    
    def authenticate(self, username=None, password=None):
        kwargs = {'email': username}
        try:
            user = TblVendor.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except TblVendor.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return TblVendor.objects.get(pk=user_id)
        except TblVendor.DoesNotExist:
            return None