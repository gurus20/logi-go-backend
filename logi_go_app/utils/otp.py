import string
import secrets

def generate_otp():
    digits = string.digits
    otp = ''.join(secrets.choice(digits) for i in range(6))
    return otp
