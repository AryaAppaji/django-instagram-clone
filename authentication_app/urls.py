from django.urls import path
from .views import AuthViewSet

urlpatterns = [
    path('login/', AuthViewSet.as_view({'post':'loginUser'})),
    path('logout/', AuthViewSet.as_view({'post':'logoutUser'})),
]