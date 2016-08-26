from django.conf.urls import url
from django.views.generic import TemplateView
from views import RegisterView
from views import StudentLoginView

urlpatterns = [
      
    url(r'^register/', RegisterView.as_view(), name="register"),
    url(r'^login/', StudentLoginView.as_view(), name="login"),

]
