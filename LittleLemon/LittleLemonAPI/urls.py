from django.urls import path, include
from . import views

urlpatterns = [
    path('users/', include('djoser.urls')),
    path('users/', include('djoser.urls.authtoken')),
    path('menu-items', views.MenuItemView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('groups/manager/users', views.manageUserView),
    path('groups/manager/users/<int:id>', views.deleteUserFromGroup),
    path('groups/delivery-crew/users', views.manageDeliveryCrewView),
    path('groups/delivery-crew/users/<int:id>', views.deleteUserFromDeliveryCrew),
    path('cart/menu-items', views.CartView.as_view()),
    path('orders', views.OrderView.as_view()),
    path('orders/<int:pk>', views.SingleOrderView.as_view()),
]