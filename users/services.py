from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model,authenticate

User= get_user_model()

def register_user(validated_data):
    user = User.objects.create_user(**validated_data)
    return user

def login_user(username,password):
    user = authenticate(username=username,password=password)
    if not user:
        raise AuthenticationFailed("Credenciales incorrectas")
    session=RefreshToken.for_user(user)
    return {
        'refresh_token':str(session),
        'access_token':str(session.access_token),
        'user':{
            'id':user.id,
            'user':user.username,
            'email': user.email
        }
    }

def logout_user(refresh_token):
    try:
        RefreshToken(refresh_token).blacklist()
    except Exception:
        raise AuthenticationFailed("Tóken inválido o expirado")