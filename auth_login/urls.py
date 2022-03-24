from django.urls import path

from .views import signin, log_out, signup


urlpatterns = [
    path('login/', signin),
    path('logout/', log_out),
    path('signup/', signup),


]