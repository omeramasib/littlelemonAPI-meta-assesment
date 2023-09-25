from django.shortcuts import render
from rest_framework import generics
from .models import MenuItem, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, UserSerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
# Create your views here.
class MenuItemView(generics.ListCreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = (IsAuthenticated,)
    ordering_fields=['price']
    search_fields=['title','category__title']

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = (IsAuthenticated,)
    throttle_classes = [AnonRateThrottle, UserRateThrottle]



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

class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    ordering_fields=['price', 'quantity', 'unit_price']
    search_fields=['menuitem__title']


    def get(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.filter(user=user)
        return Response(CartSerializer(cart, many=True).data)

    def delete(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.filter(user=user)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    ordering_fields=['total']

    def get(self, request, *args, **kwargs):
        user = request.user
        manager = Group.objects.get(name='Manager')
        delivery_crew = Group.objects.get(name='Delivery crew')
        if user in manager.user_set.all():
            orders = Order.objects.all()
            return Response(OrderSerializer(orders, many=True).data)
        elif user in delivery_crew.user_set.all():
            orders = Order.objects.filter(delivery_crew=user).all()
            return Response(OrderSerializer(orders, many=True).data)
        else:
            orders = Order.objects.filter(user=user)
            return Response(OrderSerializer(orders, many=True).data)


class SingleOrderView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        user = request.user
        if order.user == user or user.groups.filter(name='Manager').exists():
            serializer = self.get_serializer(order)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def put(self, request, *args, **kwargs):
        order = self.get_object()
        user = request.user
        if order.user == user or user.groups.filter(name='Manager').exists():
            serializer = self.get_serializer(order, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        user = request.user

        if user.groups.filter(name='Delivery crew').exists():
            if 'status' in request.data and len(request.data.keys()) == 1:
                new_status = request.data.get('status')
                order.status = new_status
                order.save()
                return Response(OrderSerializer(order).data)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)

        elif order.user == user or user.groups.filter(name='Manager').exists():
            serializer = self.get_serializer(order, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


    def delete(self, request, *args, **kwargs):
        order = self.get_object()
        if request.user.groups.filter(name='Manager').exists():
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


