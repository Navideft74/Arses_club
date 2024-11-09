from kavenegar import KavenegarAPI, APIException, HTTPException
from django.conf import settings

def kavenegar_send_otp(mobile, otp):
    """
    Sends an OTP via Kavenegar API to the specified mobile number.
    """
    try:
        api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
        params = {
            'sender': '',  # Optional: Specify a sender number if desired
            'receptor': mobile,
            'message': f'رمز ورود شما {otp}'
        }
        api.sms_send(params)
        print(f'otp ======================>>>>> {otp}')
        return True
    except (APIException, HTTPException) as e:
        print(f'Error sending OTP: {e}')
        print(f'otp ======================>>>>> {otp}')
        return True

def send_otp(otp):
    print(f'otp ======================>>>>> {otp}')