from django.urls import path
from .views import AuthViewSet

auth_view = AuthViewSet.as_view({
    'post': 'register'
})

login_view = AuthViewSet.as_view({
    'post': 'login'
})

logout_view = AuthViewSet.as_view({
    'post': 'logout'
})

urlpatterns = [
    path('auth/register/',auth_view,name='register'),
    path('auth/login/',login_view,name='login'),
    path('auth/logout/',logout_view,name='logout')

]