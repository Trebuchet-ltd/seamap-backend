from django.urls import path

from .views import signin, log_out, signup, reset_password

urlpatterns = [
    path('login/', signin),
    path('logout/', log_out),
    path('signup/', signup),
    path('password_reset/', reset_password),

]
