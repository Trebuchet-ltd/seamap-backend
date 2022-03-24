from django.urls import path

from .views import signin, log_out, signup, password_reset

urlpatterns = [
    path('login/', signin),
    path('logout/', log_out),
    path('signup/', signup),
    path('password_reset/', password_reset),

]
