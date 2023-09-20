from django.shortcuts import render
from rest_framework import generics
from .models import MenuItem
from .serializers import MenuItemSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
# Create your views here.
class MenuItemView(generics.ListCreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = (IsAuthenticated,)

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = (IsAuthenticated,)


@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser])
def managers(request):
    if request.method == 'GET':
        managers = Group.objects.get(name='Manager').user_set.all()
        return Response(UserSerializer(managers, many=True).data)
    
    elif request.method == 'POST':
        username = request.data['username']
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name='Manager')
        managers.user_set.add(user)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

