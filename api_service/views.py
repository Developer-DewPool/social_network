import jwt
import string
import random
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.conf import settings
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings
from django.db.models import Q
from rest_framework import generics, status
from .serializers import *


User = get_user_model()

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    # Generates a random string of uppercase letters and digits
    return ''.join(random.choice(chars) for _ in range(size))
    

class SignupView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data, context={'request': request})
        try:
            if serializer.is_valid():
                user = serializer.save()

                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)

                content = {
                    'error': False,
                    'message': 'Registrations successful',
                    'token': token,
                    'data': serializer.data,
                }
                return Response(content, status=status.HTTP_201_CREATED)
            else:
                content = {
                    'error': True,
                    'message': 'Email address already exists',
                }
                return Response(content, status=status.HTTP_302_FOUND)
        except KeyError:
            content = {
                'error': True,
                'message': 'Please fill the details',

            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class UserEditProfile(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        # Retrieve the authenticated user
        obj = User.objects.get(id=request.user.id)
        # Deserialize and validate the provided data for user profile update
        user_edit_serializer = UserEditSerializer(obj, data=request.data)
        user_pass_serializer = UpdatePasswordSerializer(obj, data=request.data)

        if user_edit_serializer.is_valid():
            user_edit_serializer.save()
            if user_pass_serializer.is_valid():
                user_pass_serializer.save()

            # Construct response content
            content = {
                'error': False,
                'message': 'success',
                'data': user_edit_serializer.data
            }

            return Response(content, status=status.HTTP_200_OK)
        else:
            # Handle invalid profile data
            return Response(user_edit_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        # Retrieve email and password from request data
        email = request.data.get('email')
        password = request.data.get('password')
        user_email = User.objects.filter(email=email).exists()

        if user_email is True:
            try:
                # Verify user exists and password is correct
                user = User.objects.get(email=email)
                pass_vaild = user.check_password(password)
                user_status = False
                user_data = {}
                token = ''
                if pass_vaild:
                    # Generate JWT token for the user
                    user_status = True
                    payload = jwt_payload_handler(user)
                    token = jwt.encode(payload, settings.SECRET_KEY)

                    # Construct user data and response content
                    user_data = {
                        'id': user.id,
                        'email': user.email,
                        'name': user.name
                    }

                    user_details = {
                        'error': False,
                        'data': user_data,
                        'token': token,
                        'status': user_status,
                    }
                    return Response(user_details, status=status.HTTP_200_OK)
                else:
                    # Handle invalid password
                    user_details = {
                        'error': False,
                        'message': 'Invaild Email or Password'
                    }
                    return Response(user_details, status=status.HTTP_400_BAD_REQUEST)

            except KeyError:
                # Handle KeyError
                content = {
                    'error': True,
                    'message': 'please provide a email or a password'
                    }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Handle invalid Email
            user_details = {
                'error': True,
                'message': 'Invaild Email'
            }
            return Response(user_details, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        try:
            email = request.data.get('email')
            temp_password = id_generator()
            user_data = User.objects.get(email=email)
            password = make_password(temp_password)
            if user_data:
                User.objects.filter(email__exact=email).update(password=password)
                # Construct response content
                content = {
                    'error': False,
                    'message': 'Temporary Password has been updated successful',
                    'temp_password': temp_password
                }
                return Response(content, status=status.HTTP_200_OK)
        except:
            # Handle invalid email
            content = {
                'error': True,
                'message': 'Invaild Email'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            email = request.data.get('email')
            passwd = request.data.get('password')
            password = make_password(passwd)
            user_data = User.objects.get(email=email)
            
            if user_data:
                User.objects.filter(email__exact=email).update(password=password)
                content = {
                    'error': False,
                    'action': 'Password has been reset successful'
                }
                return Response(content, status=status.HTTP_200_OK)
        except:
            content = {
                'error': True,
                'message': 'Invaild Email'
            }
            return Response(content, status=status.HTTP_200_OK)


class UserSearchView(generics.ListAPIView):
    # Specify the serializer class to convert User model instances into JSON
    serializer_class = UserSerializer
    # Require the user to be authenticated to access this view
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        '''
        Override the default get_queryset method to filter the User objects
        based on the 'query' parameter from the request's query parameters.
        '''
        # Retrieve the 'query' parameter from the request's query parameters and convert to lowercase
        query = self.request.query_params.get('q', '').lower()
        try:
            # Check if the query contains '@', indicating an email search
            if '@' in query:
                # Return a queryset filtered by exact email match, case insensitive
                return User.objects.filter(email__iexact=query)
            
            # Otherwise, return a queryset filtered by partial username match, case insensitive
            return User.objects.filter(name__icontains=query)
        except:
            content = {
                'error': True,
                'message': 'Bad Request'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class FriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get the user sending the request
        from_user = request.user
        # Get the user to whom the request is being sent
        to_user_id = request.data.get('to_user')
        try:
            to_user = User.objects.get(id=to_user_id)
            # Check if a pending friend request already exists between these users
            if FriendRequest.objects.filter(from_user=from_user, to_user=to_user, status='pending').exists():
                content = {
                    'error': False,
                    'message': 'Friend request already sent'
                    }

                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            # Create a new friend request
            FriendRequest.objects.create(from_user=from_user, to_user=to_user)
            content = {
                'error': False,
                'message': 'Friend request sent'
            }
            
            return Response(content, status=status.HTTP_201_CREATED)
        except:
            content = {
                'error': True,
                'message': 'Bad Request'
            }
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            # Get the friend request by ID
            friend_request = FriendRequest.objects.get(id=pk)
        except FriendRequest.DoesNotExist:
            content = {
                'error': True,
                'message': 'Friend request not found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)

        # Ensure the logged-in user is the recipient of the friend request
        if friend_request.to_user != request.user:
            content = {
                'error': False,
                'message': f"Friend request {new_status}"
            }
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        # Get the new status from the request data
        new_status = request.data.get('status')
        if new_status in ['accepted', 'rejected']:
            # Save a friend request if the request is accepted or rejected
            friend_request.status = new_status
            friend_request.save()
            content = {
                'error': True,
                'message': 'Unauthorized'
            }
            return Response(content, status=status.HTTP_200_OK)
        # If the status is invalid, return a bad request response
        content = {
                'error': True,
                'message': 'Invalid status'
        }
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            # Get the friend request by ID
            friend_request = FriendRequest.objects.get(id=pk)
        except FriendRequest.DoesNotExist:
            content = {
                'error': True,
                'message': 'Friend request not found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        # Ensure the logged-in user is either the sender or recipient of the friend request
        if friend_request.from_user != request.user and friend_request.to_user != request.user:
            content = {
                'error': True,
                'message': 'Unauthorized'
            }
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        # If the friend request was accepted, delete the corresponding friendship
        if friend_request.status == 'accepted':
            FriendRequest.objects.filter(
                (Q(from_user=friend_request.from_user) & Q(to_user=friend_request.to_user)) |
                (Q(to_user=friend_request.to_user) & Q(from_user=friend_request.from_user))
            ).delete()
        # Delete the friend request
        friend_request.delete()
        content = {
            'error': False,
            'message': 'Friend request deleted'
        }
        return Response(content, status=status.HTTP_200_OK)


class FriendListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(
            Q(sent_requests__to_user=user, sent_requests__status='accepted') | 
            Q(received_requests__from_user=user, received_requests__status='accepted')
            ).distinct()


class PendingRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(to_user=user, status='pending')