from django.contrib.auth.base_user import BaseUserManager

class MyUserManager(BaseUserManager):
    """
    Custom manager for creating users and superusers. Handles the logic for user creation
    based on the mobile number and optional password (since OTP-based login is used).
    """

    def create_user(self, mobile, password=None, **otherfields):
        """
        Create and return a regular user with the given mobile number. Optionally, a password 
        can be set, but typically the OTP system doesn't require it.

        Args:
            mobile (str): Mobile number (unique field for authentication).
            password (str, optional): Password for the user (defaults to None).
            **otherfields: Any additional fields for user creation (such as profile info).

        Returns:
            MyUser: The created user object.
        """
        if not mobile:
            raise ValueError('Mobile is required')  # Mobile number is mandatory
        
        # Create the user instance with the provided mobile and other fields
        user = self.model(mobile=mobile, **otherfields)
        print(f"Debug: Creating user with mobile: {mobile}")
        
        # OTP-based login, no password is necessary unless you choose to use it
        # Uncomment if password is needed in the future
        # if password:
        #     user.set_password(password)
        
        user.save()  # Save the user to the database
        print(f"Debug: User created with ID: {user.id}")  # Debug: Confirm the user creation
        return user

    def create_superuser(self, mobile, password=None, **otherfields):
        """
        Create and return a superuser with the given mobile number. A superuser is an admin 
        with staff, superuser, and active status enabled by default.

        Args:
            mobile (str): Mobile number (unique field for authentication).
            password (str, optional): Password for the user (defaults to None).
            **otherfields: Any additional fields for superuser creation.

        Returns:
            MyUser: The created superuser object.
        """
        # Set default values for staff, superuser, and active fields
        otherfields.setdefault('is_staff', True)
        otherfields.setdefault('is_superuser', True)
        otherfields.setdefault('is_active', True)

        # Ensure that the user is marked as staff, superuser, and active
        if otherfields.get('is_staff') is not True:
            raise ValueError('Must have staff=True')
        if otherfields.get('is_active') is not True:
            raise ValueError('Must have active=True')
        if otherfields.get('is_superuser') is not True:
            raise ValueError('Must have superuser=True')
        
        # Call the create_user method to create the superuser
        return self.create_user(mobile, password, **otherfields)


# from django.contrib.auth.base_user import BaseUserManager


# class MyUserManager(BaseUserManager):

#     # def create_user(self, mobile, password=None, **otherfields):
#     #     if not mobile:
#     #         raise ValueError('mobile is required')
#     #     user = self.model(mobile=mobile, **otherfields)
#     #     # user.set_password(password)
#     #     user.save()
#     #     return user
#     def create_user(self, mobile, password=None, **otherfields):
#         if not mobile:
#             raise ValueError('Mobile is required')
        
#         user = self.model(mobile=mobile, **otherfields)
#         print(f"Debug: Creating user with mobile: {mobile}")
        
#         # Set password if needed; otherwise, leave commented for OTP-based login
#         # user.set_password(password)
        
#         user.save()
#         print(f"Debug: User created with ID: {user.id}")
#         return user

#     def create_superuser(self, mobile, password=None, **otherfields):
#         otherfields.setdefault('is_staff', True)
#         otherfields.setdefault('is_superuser', True)
#         otherfields.setdefault('is_active', True)

#         if otherfields.get('is_staff') is not True:
#             raise ValueError('Must have staff=true')
#         if otherfields.get('is_active') is not True:
#             raise ValueError('Must have active=true')
#         if otherfields.get('is_superuser') is not True:
#             raise ValueError('Must have superuser=true')
#         return self.create_user(mobile, password, **otherfields)