from django.urls import path, include
from . import views

urlpatterns = [
    # path('ratings', views.RatingsView.as_view()),
    path('users/', include('djoser.urls')),
    path('users/', include('djoser.urls.authtoken')),
    path('menu-items', views.MenuItemView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('groups/manager/users', views.manageUserView),
    path('groups/manager/users/<int:id>', views.deleteUserFromGroup),
    path('groups/delivery-crew/users', views.manageDeliveryCrewView),
    path('groups/delivery-crew/users/<int:id>', views.deleteUserFromDeliveryCrew),
]