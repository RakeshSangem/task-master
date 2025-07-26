from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken

from todo.apps.users.serializers import UserRegisterSerializer, UserLoginSerializer
from todo.apps.users.models import User


def create_token_for_user(user):
    """ Pure function to create a token for a user """
    refresh = RefreshToken.for_user(user)
    return {
        'message': 'Token created successfully',
        'user': get_user_data(user),
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


def get_user_data(user):
    """ Pure function to get user data """
    return {
        'id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name
    }


def validate_user_credentials(email, password):
    """ Pure function to validate user credentials """

    if not email or not password:
        return None, "Email and password are required"

    try:
        user = User.objects.get(email=email)

        if user and user.check_password(password):
            return user, None
        return None, "Invalid credentials"
    except Exception as e:
        return None, str(e)


class RegisterView(generics.CreateAPIView):
    """
    POST /api/users/register/ - Register a new user
    """
    serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(create_token_for_user(user), status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    """
    POST /api/login/ - Login a user
    """
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token = create_token_for_user(user)
        user_data = get_user_data(user)

        return Response({
            'message': 'Login successful',
            'user': user_data,
            'refresh': token['refresh'],
            'access': token['access']
        }, status=status.HTTP_200_OK)
