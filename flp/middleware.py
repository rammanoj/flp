import pytz
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone


class TimezoneMiddleware(MiddlewareMixin):

    # The Middleware localises the TimeZone, so that the input time will be stored in the timezone specified.
    def process_request(self, request):
        timezone.activate(pytz.timezone('Asia/Kolkata'))