from django.conf.urls import url
from django.views.generic import TemplateView
from ..views import *
from ..forms import StudentForm, StudentLoginForm, PasswordResetRequestForm, PasswordResetConfirmForm
urlpatterns = [
      
    url(r'^register/$', RegisterView.as_view(form_class=StudentForm,
                                      template_name='student_registration.html',
                                      success_url='#', role='student'),
                                      name="register"),

    url(r'^login/$', LoginView.as_view(form_class=StudentLoginForm,
                                      template_name='student_login.html',
                                      success_url='#', role='student' 
                                       ), name="login"),

    url(r'^activities/$', StudentActivitiesView.as_view(), name="activities"),

    url(r'^activity/details/(?P<pk>\d+)/$', ActivityDetailsView.as_view(role='student', 
                template_name='student_activity_details.html'), name="activity-details"),

    url(r'^profile/$', StudentProfileView.as_view(), name="profile"),

    url(r'^about/$', ScadiilAboutView.as_view(), name="about"),
    
    url(r'^logout/$', LogoutView.as_view(), name="logout" ),

    url(r'^reset_password/$', PasswordResetRequestView.as_view(form_class=PasswordResetRequestForm,
                                      template_name='password_reset_form.html',
                                      success_url='#', role='student'),
                                      name="password_reset_request"),

    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', \
                                      PasswordResetConfirmView.as_view(form_class=PasswordResetConfirmForm,
                                      template_name='password_reset_confirm.html',
                                      success_url='#', role='student'),
                                      name="password_reset_confirm"),

]
