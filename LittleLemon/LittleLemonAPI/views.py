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
def manageUserView(request):
    if request.method == 'GET':
        managers = Group.objects.get(name='Manager').user_set.all()
        return Response(UserSerializer(managers, many=True).data)

    elif request.method == 'POST':
        username = request.data['username']
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name='Manager')
        managers.user_set.add(user)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUserFromGroup(request, id):
    user = get_object_or_404(User, id=id)
    managers = Group.objects.get(name='Manager')
    if user in managers.user_set.all():
        managers.user_set.remove(user)
        return Response(status=status.HTTP_200_OK, data={'message': 'Sucsses'})
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', 'GET'])
@permission_classes([IsAdminUser])
def manageDeliveryCrewView(request):
    if request.method == 'GET':
        managers = Group.objects.get(name='Delivery crew').user_set.all()
        return Response(UserSerializer(managers, many=True).data)

    elif request.method == 'POST':
        username = request.data['username']
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name='Delivery crew')
        managers.user_set.add(user)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUserFromDeliveryCrew(request, id):
    user = get_object_or_404(User, id=id)
    managers = Group.objects.get(name='Delivery crew')
    if user in managers.user_set.all():
        managers.user_set.remove(user)
        return Response(status=status.HTTP_200_OK, data={'message': 'Sucsses'})
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
