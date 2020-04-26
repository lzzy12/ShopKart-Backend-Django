from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .permissions import IsCreatorOrReadOnly, IsUnAuthenticated
from .serializers import ProductsSerializer, UserSerializer


class ProductsListView(generics.ListCreateAPIView):
    serializer_class = ProductsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        queryset = Product.objects.all()
        if username is not None:
            queryset = queryset.filter(creator__username=username)
        return queryset

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class ProductItemView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductsSerializer
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCreatorOrReadOnly]


class LoginView(APIView):
    def post(self, request: Request):
        username = self.request.data.get('username')
        password = request.data.get('password')
        if username is None or password is None:
            return Response({'error': 'No valid credentials found in the request'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        user = UserSerializer(instance=user)
        return Response({'token': token.key, 'user': user.data}, status=status.HTTP_200_OK)


class SignUpView(APIView):
    permission_classes = [IsUnAuthenticated]

    def post(self, request: Request):
        username = self.request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        if username is None or password is None or email is None:
            return Response({'error': 'Credentials Invalid'}, status=status.HTTP_400_BAD_REQUEST)
        serialized = UserSerializer(data=request.data)
        if serialized.is_valid():
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            token = Token.objects.create(user=user)
            serialized = UserSerializer(instance=user)
            return Response({'token': token.key, 'user': serialized.data})
        else:
            return Response({'error': serialized.errors}, status=status.HTTP_400_BAD_REQUEST)
