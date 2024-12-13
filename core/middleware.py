# middleware.py  
from django.utils import timezone  
from django.conf import settings  
from rest_framework.authtoken.models import Token  
from django.contrib.auth.models import User  
from rest_framework.response import Response  
from django.utils.deprecation import MiddlewareMixin  

class InactivityLogoutMiddleware(MiddlewareMixin):  
    def process_request(self, request):  
        # Define the inactivity timeout (in seconds)  
        inactivity_timeout = getattr(settings, 'INACTIVITY_TIMEOUT', 300)  # Default to 5 minutes  

        if request.user.is_authenticated:  
            # Check the last activity time  
            last_activity = request.session.get('last_activity')  

            # If last_activity is None, set it to now  
            if last_activity is None:  
                request.session['last_activity'] = timezone.now().timestamp()  
            else:  
                # Calculate the time since the last activity  
                if timezone.now().timestamp() - last_activity > inactivity_timeout:  
                    # Log the user out if the inactivity timeout has been exceeded  
                    token = request.auth  # Get the token from the request  
                    if token:  
                        try:  
                            token_obj = Token.objects.get(key=token)  
                            token_obj.delete()  # Delete the token to log the user out  
                        except Token.DoesNotExist:  
                            pass  

                    # Clear the session and return a response  
                    request.session.flush()  # Clear session data  
                    return Response({'error': 'You have been logged out due to inactivity.'}, status=401)  

            # Update the last activity time  
            request.session['last_activity'] = timezone.now().timestamp()