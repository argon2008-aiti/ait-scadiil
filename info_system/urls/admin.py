from django.conf.urls import url
from django.contrib.auth import views
from django.views.generic import TemplateView
from ..views import * 
from ..forms import StudentForm, EnrolStudentForm
from ..forms import AdminLoginForm, PasswordResetRequestForm, PasswordResetConfirmForm
urlpatterns = [

    url(r'^students/all/$', StudentView.as_view(role='admin'), name="students-all"),

    url(r'^students/details/(?P<pk>\d+)/$', StudentDetailsView.as_view(role='admin'), name="student-details"),

    url(r'^students/completion-list/$', ScadiilCompletionView.as_view(role='admin'), name="students-complete"),
    
    url(r'^internship/pre-interns/$', PreInternStudentView.as_view(role='admin'), name="internship-pre-interns"),

    url(r'^internship/at-post/$', StudentsAtPostView.as_view(role='admin'), name="internship-at-post"),

    url(r'^internship/returnees/$', ReturneeStudentsView.as_view(role='admin'), name="internship-returnee"),

    url(r'^internship/completion-list/$', InternshipCompletionView.as_view(role='admin'),
                                name="internship-complete"),

    url(r'^courses/ufs/$', UFSView.as_view(role='admin'), name="courses-ufs"),

    url(r'^courses/ufs/new$', UFSNewGrade.as_view(role='admin'), name="ufs-new"),

    url(r'^courses/ufs/new/review$', GradeListView.as_view(role='admin', course='ufs'), name="ufs-review"),

    url(r'^courses/cdes/$', CDESView.as_view(role='admin'), name="courses-cdes"),

    url(r'^courses/cdes/new$', CDESNewGrade.as_view(role='admin'), name="cdes-new"),

    url(r'^courses/cdes/new/review$', GradeListView.as_view(role='admin', course='cdes'), name="cdes-review"),

    url(r'^activities/$', AdminActivitiesView.as_view(role='admin'), name="activities"),

    url(r'^activities/new$', NewActivitiesView.as_view(role='admin'), name="activities-new"),

    url(r'^activity/details/(?P<pk>\d+)/$', ActivityDetailsView.as_view(role='admin'), name="activity-details"),
    
    url(r'^messages/$', MessagesView.as_view(role='admin'), name="messages"),

    url(r'^statistics/$', StatsView.as_view(role='admin'), name="statistics"),

    url(r'^seminars/all/$', SeminarAllView.as_view(role='admin'), name="seminars-all"),

    url(r'^upload/ufs$', SaveGrade.as_view(role='admin', course="ufs")),

    url(r'^upload/cdes$', SaveGrade.as_view(role='admin', course="cdes")),

    url(r'^seminars/new/$', SeminarNewView.as_view(role='admin'), name="seminar-new"),

    url(r'^seminars/upcoming/$', UpcomingSeminarView.as_view(role='admin'), name="seminars-upcoming"),

    url(r'^seminars/past/$', PastSeminarView.as_view(role='admin'), name="seminars-past"),

    url(r'^seminars/attendance/(?P<pk>\d+)/$', NewSeminarAttendanceView.as_view(role='admin')),

    url(r'^seminars/edit/(?P<pk>\d+)/$', EditSeminarView.as_view(role='admin')),

    url(r'^seminars/attendance/(?P<pk>\d+)/new/review/$', AttendanceListView.as_view(role='admin')),

    url(r'^seminar/(?P<pk>\d+)/attendance/upload/$', SaveAttendanceView.as_view(role='admin')),
    
    url(r'^seminars/details/(?P<pk>\d+)/$', DetailSeminarView.as_view(role='admin'), name="seminar-details"),

    url(r'^capstone/proposal/$', CapstoneProposalView.as_view(role='admin'), name="capstone-proposal"),

    url(r'^capstone/part-one/$', CapstonePartOneView.as_view(role='admin'), name="capstone-part-one"),

    url(r'^capstone/part-two/$', CapstonePartTwoView.as_view(role='admin'), name="capstone-part-two"),

    url(r'^capstone/viva/$', CapstoneVivaView.as_view(role='admin'), name="capstone-viva"),

    url(r'^capstone/completion-list/$', CapstoneCompletionListView.as_view(role='admin'),
                                               name="capstone-complete"),
      
    url(r'^students/enrol/$', EnrolStudentView.as_view(form_class=EnrolStudentForm,
                                      template_name='enrol_student.html',
                                       success_url='../all', role='admin'), name="enrol-student"),

    url(r'^login/$', LoginView.as_view(form_class=AdminLoginForm,
                                      template_name='admin_login.html',
                                      success_url='#', role='admin'), name="login"),

    url(r'^logout/$', LogoutView.as_view(), name="logout" ),

    url(r'^reset_password/$', PasswordResetRequestView.as_view(form_class=PasswordResetRequestForm,
                                      template_name='password_reset_form.html',
                                      success_url='#', role='admin'),
                                      name="password_reset_request"),

    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', \
                                      PasswordResetConfirmView.as_view(form_class=PasswordResetConfirmForm,
                                      template_name='password_reset_confirm.html',
                                      success_url='#', role='admin'),
                                      name="password_reset_confirm"),

]
