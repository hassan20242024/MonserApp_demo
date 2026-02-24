from .views import SignUpView, SignInView,SignOutView ,BienvenidaView
from django.urls import path

from . import views
urlpatterns = [
 
    path('', BienvenidaView.as_view(), name='bienvenida'),
    path('registrate/', SignUpView.as_view(), name='sign_up'),
    path('MonsterAPP/', SignInView.as_view(), name='sign_in'),
    path('cerrar-sesion/', SignOutView.as_view(), name='sign_out'),
]

