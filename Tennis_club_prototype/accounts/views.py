from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.utils import timezone
from django.contrib import messages
from .models import MyUser
import random
from .utils import kavenegar_send_otp
from datetime import timedelta

def signup_or_login(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        if not mobile:
            messages.error(request, 'Please enter a valid mobile number.')
            return redirect('signup_or_login')

        user, created = MyUser.objects.get_or_create(mobile=mobile)
        print(f"Debug: User found with mobile {mobile}: {not created}")

        otp_age_limit = timedelta(minutes=3)

        # Check if OTP was recently sent
        if not created and user.otp_created and (timezone.now() - user.otp_created) < otp_age_limit:
            messages.info(request, 'OTP was recently sent. Please check your messages.')
            return redirect('verify_otp')

        # Generate OTP and set creation time
        otp = random.randint(1000, 9999)
        user.otp = otp
        user.otp_created = timezone.now()
        user.save()
        print(f"Debug: OTP set to {user.otp} with timestamp {user.otp_created}")

        # Send OTP via SMS and store mobile in session if successful
        if kavenegar_send_otp(mobile, otp):
            request.session['mobile'] = mobile
            messages.success(request, 'OTP sent successfully!')
            return redirect('verify_otp')
        else:
            messages.error(request, 'Failed to send OTP. Please try again.')
            return redirect('signup_or_login')

    return render(request, 'accounts/signup_or_login.html')



def verify_otp(request):
    # Step 1: Check if the request method is POST, which is expected for OTP verification
    if request.method == 'POST':
        otp = request.POST.get('otp')  # Retrieve OTP from the form
        mobile = request.session.get('mobile')  # Retrieve mobile from session
        print(otp, mobile)  # Debug: Print the OTP and mobile to verify they are retrieved correctly

        # Step 2: Check if the mobile session data is available
        if not mobile:
            # If mobile is not in the session, redirect to signup/login, indicating session expiration
            messages.error(request, 'Session expired. Please start again.')
            return redirect('signup_or_login')

        # Step 3: Ensure the OTP is a valid integer; catch any ValueError if OTP is not numeric
        try:
            otp = int(otp)  # Convert OTP to integer for comparison
        except ValueError:
            # Redirect to OTP verification with an error if OTP format is invalid
            messages.error(request, 'Invalid OTP format. Please enter numbers only.')
            return redirect('verify_otp')

        # Step 4: Authenticate user using the custom backend with mobile and OTP
        user = authenticate(request, mobile=mobile, otp=otp)  # Custom backend will handle OTP validation
        if user:
            # Step 5: Clear OTP and save the user if authentication is successful
            user.otp = None  # Clear OTP to prevent reuse
            user.save()
            print('user is saved')  # Debug: Confirm user has been saved

            # Step 6: Clear the session data for mobile to maintain security
            request.session.pop('mobile', None)
            print('session is poped')  # Debug: Confirm session data has been cleared

            # Step 7: Log in the user using Django's login method
            login(request, user)  # Log the user in with the custom backend
            print('user has logged in')  # Debug: Confirm user login

            # Step 8: Check if the user’s profile is complete; redirect to profile completion if needed
            if not user.profile.first_name or not user.profile.last_name:
                # Redirect to profile completion if first or last name is missing
                messages.info(request, 'Please complete your profile information.')
                return redirect('complete_profile')

            # Step 9: Redirect to home page if login and profile are complete
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            # Handle case where OTP is invalid or expired
            messages.error(request, 'Invalid OTP or OTP has expired.')
            return redirect('verify_otp')

    # Render OTP verification page if request method is not POST
    return render(request, 'accounts/verify_otp.html')



def complete_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        if not first_name or not last_name:
            messages.error(request, 'First and last name are required.')
            return redirect('complete_profile')

        # Update the user's profile
        user = request.user
        profile = user.profile
        profile.first_name = first_name
        profile.last_name = last_name
        profile.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('home')

    return render(request, 'accounts/complete_profile.html')




def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('signup_or_login')



from .forms import ProfileForm

def update_profile(request):
    user = request.user  # Get the current logged-in user

    # If the user doesn't have a profile, you can redirect to a profile completion page (optional)
    if not hasattr(user, 'profile'):
        messages.error(request, "Profile not found. Please complete your profile.")
        return redirect('complete_profile')  # This view needs to be defined

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user.profile)  # Bind form with the existing profile data
        if form.is_valid():
            form.save()  # Save the updated profile data
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')  # Redirect to the profile view (you need to define this view)
        else:
            messages.error(request, "There was an error updating your profile.")
    else:
        form = ProfileForm(instance=user.profile)  # Load the form with the current profile data

    return render(request, 'accounts/update_profile.html', {'form': form})
