from django.contrib.auth.backends import ModelBackend
from .models import MyUser

class MobileBackend(ModelBackend):
    def authenticate(self, request, mobile=None, otp=None, **kwargs):
        # Step 1: Check for the presence of both mobile and OTP
        if not mobile or not otp:
            print("Debug: Missing mobile or OTP")  # Debugging output to detect missing parameters
            return None  # Return None if either mobile or OTP is missing

        try:
            # Step 2: Fetch the user by mobile number
            user = MyUser.objects.get(mobile=mobile)

            # Debugging outputs to validate fetched OTP and check OTP validity
            print(f"Debug: Stored OTP = {user.otp}, Provided OTP = {otp}")
            print(f"Debug: OTP valid? {user.otp_is_valid()}")

            # Step 3: Check if the provided OTP matches the stored OTP and is still valid
            if user.otp == otp and user.otp_is_valid():
                # Successful authentication
                return user
            else:
                # Either the OTP did not match or is no longer valid
                print("Debug: OTP is invalid or expired.")
                return None  # Return None if OTP check fails

        # Step 4: Handle case where user with provided mobile number doesn't exist
        except MyUser.DoesNotExist:
            print("Debug: User does not exist")  # Debugging output for non-existent user
            return None  # Return None if no user with the provided mobile number exists

    def get_user(self, user_id):
        # Step 5: Retrieve user by primary key for session persistence
        try:
            return MyUser.objects.get(pk=user_id)
        except MyUser.DoesNotExist:
            # Return None if the user with the specified ID is not found
            return None
