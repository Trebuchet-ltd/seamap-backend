from django.urls import path

from .views import go_to_dashboard, signin, log_out, signup, reset_password

urlpatterns = [
    path('', go_to_dashboard),
    path('login/', signin),
    path('logout/', log_out),
    path('signup/', signup),
    path('password_reset/', reset_password),

]
