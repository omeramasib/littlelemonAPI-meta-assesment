from django.urls import path, include
from . import views

urlpatterns = [
    # path('ratings', views.RatingsView.as_view()),
    path('users/', include('djoser.urls')),
    path('users/', include('djoser.urls.authtoken')),
    path('menu-items', views.MenuItemView.as_view()),
]