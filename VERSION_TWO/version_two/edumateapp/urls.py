from django.conf.urls import url
from edumateapp import views


app_name = "edumateapp"

urlpatterns = [
    url(r"^register/$", views.register, name="register"),
    url(r"^user_login/$", views.user_login, name="user_login"),
]
