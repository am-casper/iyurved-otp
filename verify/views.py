import json
import random
import uuid
from django.shortcuts import render
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from verify.models import User
from rest_framework.authtoken.models import Token
from django.core.cache import cache

from verify.serializers import UserSerializer

@api_view(['POST'])
def initiate_auth(request):
    phone_number = request.data.get('phone_number')
    if not phone_number:
        return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST) 


    user, created = User.objects.get_or_create(phone_number=phone_number) 

    if (phone_number !='9999999999'):
        # Generate OTP
        otp = random.randint(100000, 999999)

        # Send OTP using your API
        res = send_otp(phone_number, otp)
        print(res)
    else:
        otp = 999999
    

    # Generate a temporary identifier
    temp_id = str(uuid.uuid4())

    # Store OTP and phone number in cache
    cache.set(temp_id, {'otp': otp, 'phone_number': phone_number}, timeout=300)

    if created:
        message = 'OTP sent for registration'
    else:
        message = 'OTP sent for login'
    print('The OTP is:', otp)
    print('The temp_id is:', temp_id)
    return Response({'message': message, 'temp_id': temp_id}, status=status.HTTP_200_OK)  # Send temp_id to the frontend

@api_view(['POST'])
def verify_otp(request):
    otp = request.data.get('otp')
    temp_id = request.data.get('temp_id')

    if not all([otp, temp_id]):
        return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)

    # Retrieve data from cache using temp_id
    cached_data = cache.get(temp_id)
    if not cached_data:
        return Response({'error': 'Invalid or expired request'}, status=status.HTTP_400_BAD_REQUEST)

    stored_otp = cached_data.get('otp')
    phone_number = cached_data.get('phone_number')

    if otp.strip() == str(stored_otp):
        user = User.objects.get(phone_number=phone_number)

        # Clear cached data after successful verification
        cache.delete(temp_id)

        return Response({
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

def send_otp(to, otp):
    # to is the phone number to which OTP will be sent converted to int
    to = [int(to)]
    body = {
            "to": to,
            "message": f"To login into your Iyurved account OTP is: {otp}. Please do not share this code with anyone. \n\nRegards, \nIyurvedAAC Team",
            "route": "otp",
            "sender_id": "IYURVD",
            "template_id": "-psW3EXIR",
    }
    api_key = "874c80b5-b88c-4286-bbdf-424b2d22f1b1"
    response = requests.post(f"https://api.trustsignal.io/v1/sms?api_key={api_key}", headers={"Content-Type": "application/json"}, data=json.dumps(body))
    return response.json()