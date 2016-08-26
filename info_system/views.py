from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.views.generic.edit import FormView 
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import View
from django.views.generic import TemplateView
from django.contrib.auth.models import User, Group
from django.contrib import messages

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from braces.views import LoginRequiredMixin, GroupRequiredMixin

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template import loader
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings

from forms import StudentForm
from forms import StudentLoginForm
from models import * 

from datetime import datetime

class ContextDataProviderMixin(object):
    role = None
    reset_url = None

    def get_context_data(self, **kwargs):
        context = super(ContextDataProviderMixin, 
                        self).get_context_data(**kwargs)
        navbar_admin = ''
        navbar_admin_brand = ''
        title   = 'AIT SCADIIL'
        logout  = 'student:logout'

        if self.role == 'admin':
            navbar_admin = 'navbar-admin'
            navbar_admin_brand = 'navbar-admin-brand'
            title   = 'SCADIIL ADMIN'
            logout  = 'admin:logout'

        context["navbar_admin"] = navbar_admin
        context["navbar_admin_brand"] = navbar_admin_brand
        context["title"]  = title
        context["logout"] = logout
        return context

class StudentListMixin(object):

    def get_context_data(self, **kwargs):
        context = super(StudentListMixin, 
                        self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        total = queryset.count()
        sates = queryset.filter(program=1).count()
        asdass = queryset.filter(program=2).count()
        abs_ = queryset.filter(program=3).count()
        context['total'] = total
        context['sates'] = sates
        context['asdass'] = asdass
        context['abs'] = abs_
        return context

class LogoutView(ContextDataProviderMixin, View):

    def get(self, request, *args, **kwargs):
        managers = Group.objects.get(name='managers')
        isAdmin = managers in self.request.user.groups.all() or self.request.user.is_superuser
        logout(self.request)
        if isAdmin: 
            print "admin logging out"
            return redirect("admin:login")

        else: 
            print "student logging out"
            return redirect("student:login")

class RegisterView(ContextDataProviderMixin, FormView):

    def form_valid(self, form):
        # create a user object from form info
        try:
            user = User.objects.create_user(first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['surname'],
                        username=form.cleaned_data['id_number'].upper(),
                        email=form.cleaned_data['email_address'],
                        password=form.cleaned_data['password'])
            student_group, created = Group.objects.get_or_create(name="student group") 
            user.groups.add(student_group)
            print "student added to group successfully"

        except IntegrityError as e:
            print "Exception Caught!"
            print e.message
            if 'UNIQUE constraint' or 'unique constraint' in e.message:
                # add ID not available error to messages
                messages.error(self.request, 'There was a problem enrolling your profile; Please \
                               review the data you provided for errors! If you need help, please \
                               contact the numbers provided at the bottom of the page.',
                               extra_tags='id_available')
                print "ID Exists"
            return super(RegisterView, self).form_invalid(form)

        # create the student object
        student = Student(user=user, middle_name=form.cleaned_data['middle_name'],
                          phone_number=form.cleaned_data['phone_number'],
                          program=form.cleaned_data['program'])
        student.save()

        return super(RegisterView, self).form_valid(form)

    def form_invalid(self, form):
        print "form not valid" 
        messages.error(self.request, 'There are issues with your form! Please correct them.')
        return super(RegisterView, self).form_invalid(form)


class LoginView(ContextDataProviderMixin, FormView):

    def get(self, request, *args, **kwargs):
        if self.request.user is not None and self.request.user.is_authenticated(): 
            if self.role == 'admin':
                return redirect("admin:activities")
            elif self.role == 'student':
                return redirect("student:activities")
        return super(LoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        if self.role=='student':
            user = authenticate(username=form.cleaned_data['id_number'].upper(), \
                                password=form.cleaned_data['password'])
            if user is None: 
                messages.error(self.request, 'ID number and Password do not match any enrolled student',\
                               extra_tags='student_login_incorrect')
                print "username and password incorrect"
                self.form_invalid(form)
            else:
                if user.is_active:
                    print "Hooray!!!"
                    login(self.request, user)
                    print "login successful"
                    return super(LoginView, self).form_valid(form)
                    if self.request.POST.has_key('next'):
                        if self.request.POST['next']!='':
                            return redirect(self.request.POST['next'])
                        else:
                            pass
                    return redirect("student:activities")
                else:
                    self.form_invalid(form)

        elif self.role=='admin':
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            # Only log system admins into the admin interface
            if user is not None: 
                try:
                    user_is_manager = user.groups.get(name="managers") is not None
                except Group.DoesNotExist as e:
                    user_is_manager = False
                    print e.message
                if (user.is_superuser or user_is_manager) and user.is_active:
                    login(self.request, user)
                    print "login successful"
                    if self.request.POST.has_key('next'):
                        if self.request.POST['next']!='':
                            return redirect(self.request.POST['next'])
                        else:
                            pass
                    return redirect("admin:students-all")
                else: 
                    messages.error(self.request, 'You do not have enough priviledges to use this interface',\
                                   extra_tags='admin_login_incorrect')
                    print "Not enough priviledges"
                    return super(LoginView, self).form_invalid(form)

            else: 
                messages.error(self.request, 'Username and Password do not match any Admin account',\
                               extra_tags='admin_login_incorrect')
                print "username and password incorrect"
                return super(LoginView, self).form_invalid(form)
        
    def form_invalid(self, form):
        print 'form is not valid'
        return super(LoginView, self).form_invalid(form)


# This view is called when a request is made for reset of password
class PasswordResetRequestView(ContextDataProviderMixin, FormView): 
        
    def form_valid(self, form):
        # get the email address that was supplied
        email = form.cleaned_data['email_address']
        associated_user = User.objects.filter(email=email)
        
        # Is there a user associated with that email
        if len(associated_user) is not 0:
            if self.role=='student':
                identification_name = 'ID Number'
                reset_url = 'student:password_reset_confirm'
            else:
                identification_name = 'Username'
                reset_url = 'admin:password_reset_confirm'
            # we could have more than 1 user with that email-- :-) some students are crazy
            print "user associated"
            print associated_user
            for user in associated_user:
                c = {
                    'email': user.email,
                    'domain': self.request.META['HTTP_HOST'],
                    'site_name': 'SCADIIL',
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'user': user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    'identification_name': identification_name,
                    'password_reset_confirm': reset_url,
                    'username': user.get_username()
                } 
                print user.get_username() 
                email_template_name = 'password_reset_email.html'
                subject_template_name = 'password_reset_subject.txt'

                email = loader.render_to_string(email_template_name, c)
                subject = loader.render_to_string(subject_template_name, c)

                subject = ''.join(subject.splitlines())

                send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

                # display a success message to client
                messages.success(self.request, "An email has been sent to the email address you provided. \
                                 Please check your inbox to continue with the password reset process.",\
                                 extra_tags='email_send_success')
            return super(PasswordResetRequestView, self).form_valid(form)

        else:
            # no user is associated with that email
            messages.error(self.request, "The email address you provided is not associated with \
                           any enrolled user. Are you sure you are already enrolled on SCADIIL?",\
                           extra_tags='email_send_error')
            return super(PasswordResetRequestView, self).form_invalid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There are issues with the data you provided. Please review them \
                       and resubmit.",  extra_tags='form-error')
        return super(PasswordResetRequestView, self).form_invalid(form)


class PasswordResetConfirmView(ContextDataProviderMixin, FormView):

    def post(self, request, uidb64, token):

        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None

        try:
            uid = urlsafe_base64_decode(uidb64)
            print uid
            user = User.objects.get(pk=uid)
            print user
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data['password']
                user.set_password(new_password)
                user.save()
                messages.success(request, "Your password has been reset successfully.")
                return self.form_valid(form)
            else:
                messages.error(request, "There are issues with the data you provided.")
                return self.form_invalid(form)
        else:
            messages.error(request, "The password reset link is not valid or has expired.")
            return self.form_invalid(form)

class StudentView(LoginRequiredMixin, GroupRequiredMixin,  ContextDataProviderMixin, StudentListMixin, ListView):
    login_url = "/admin/login/"
    model = Student
    template_name = 'students_all.html' 
    group_required = u"managers"
    raise_exception = True


class ScadiilCompletionView(LoginRequiredMixin, ContextDataProviderMixin, StudentListMixin, ListView):
    login_url = "/admin/login/"
    model = Student
    template_name = 'scadiil_completion_list.html' 

    def get_queryset(self):
        queryset = super(ScadiilCompletionView, self).get_queryset()
        return queryset.filter(capstone__status=3, internship__status=3, seminarattendance__gte=12) 

class AdminActivitiesView(LoginRequiredMixin, GroupRequiredMixin, ContextDataProviderMixin, ListView):
    login_url = "/admin/login/"
    model = Activity
    template_name = 'activities.html' 
    group_required = u"managers"
    raise_exception = True

class MessagesView(LoginRequiredMixin, ContextDataProviderMixin, ListView):
    login_url = "/admin/login/"
    model = Message
    template_name = 'messages.html' 

class StatsView(LoginRequiredMixin, ContextDataProviderMixin, ListView):
    login_url = "/admin/login/"
    model = Message
    template_name = 'statistics.html' 

class UFSView(LoginRequiredMixin, ContextDataProviderMixin, StudentListMixin, ListView):
    login_url = "/admin/login/"
    model = Student
    template_name = 'ufs_list.html' 

    def get_queryset(self):
        queryset = super(UFSView, self).get_queryset()
        return queryset.filter(UFS_passed=True) 


class CDESView(LoginRequiredMixin, ContextDataProviderMixin, StudentListMixin, ListView):
    login_url = "/admin/login/"
    model = Student
    template_name = 'cdes_list.html' 

    def get_queryset(self):
        queryset = super(CDESView, self).get_queryset()
        return queryset.filter(CDES_passed=True) 


class PreInternStudentView(LoginRequiredMixin, ContextDataProviderMixin, StudentListMixin, ListView):
    login_url = "/admin/login/"
    model = Student
    template_name = 'internship_pre.html' 

    def get_queryset(self):
        queryset = super(PreInternStudentView, self).get_queryset()
        return queryset.filter(CDES_passed=True, UFS_passed=True, seminarattendance__gte=1) 


class StudentsAtPostView(LoginRequiredMixin, ContextDataProviderMixin, StudentListMixin, ListView):
    login_url = "/admin/login/"
    model = Student
    template_name = 'internship_at_post.html' 

    def get_queryset(self):
        queryset = super(StudentsAtPostView, self).get_queryset()
        return queryset.filter(internship=1) 

class ReturneeStudentsView(LoginRequiredMixin, ContextDataProviderMixin, StudentListMixin, ListView):
    login_url = "/admin/login/"
    model = Student
    template_name = 'internship_returnee.html' 

    def get_queryset(self):
        queryset = super(ReturneeStudentsView, self).get_queryset()
        return queryset.filter(internship__status=2) 

class InternshipCompletionView(LoginRequiredMixin, ContextDataProviderMixin, StudentListMixin, ListView):
    login_url = "/admin/login/"
    model = Student
    template_name = 'internship_completion_list.html' 

    def get_queryset(self):
        queryset = super(InternshipCompletionView, self).get_queryset()
        return queryset.filter(internship__isnull = False, internship__status=3) 

class SeminarAllView(LoginRequiredMixin, ContextDataProviderMixin, ListView):
    login_url = "/admin/login/"
    model = Seminar
    template_name = 'seminars_all.html' 

    def get_context_data(self, **kwargs):
        context = super(SeminarAllView, 
                        self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["today"] = datetime.now()
        context["sates_count"] = queryset.filter(school=1).count() 
        context["asdass_count"] = queryset.filter(school=3).count() 
        context["abs_count"] = queryset.filter(school=2).count() 
        return context


class UpcomingSeminarView(LoginRequiredMixin, ContextDataProviderMixin, ListView):
    login_url = "/admin/login/"
    model = Seminar
    template_name = 'seminars_upcoming.html' 
    def get_queryset(self):
        queryset = super(UpcomingSeminarView, self).get_queryset()
        return queryset.filter(date__gte=datetime.now())

    def get_context_data(self, **kwargs):
        context = super(UpcomingSeminarView, 
                        self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["today"] = datetime.now()
        context["sates_count"] = queryset.filter(school=1).count() 
        context["asdass_count"] = queryset.filter(school=3).count() 
        context["abs_count"] = queryset.filter(school=2).count() 
        return context

class PastSeminarView(LoginRequiredMixin, ContextDataProviderMixin, ListView):
    login_url = "/admin/login/"
    model = Seminar
    template_name = 'seminars_past.html' 
    def get_queryset(self):
        import datetime
        queryset = super(PastSeminarView, self).get_queryset()
        return queryset.filter(date__lt=datetime.datetime.now())

    def get_context_data(self, **kwargs):
        context = super(PastSeminarView, 
                        self).get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["today"] = datetime.now()
        context["sates_count"] = queryset.filter(school=1).count() 
        context["asdass_count"] = queryset.filter(school=3).count() 
        context["abs_count"] = queryset.filter(school=2).count() 
        return context

class DetailSeminarView(LoginRequiredMixin, ContextDataProviderMixin, DetailView):
    login_url = "/admin/login/"
    model = Seminar
    template_name = 'seminar_details.html' 

class CapstoneProposalView(LoginRequiredMixin, ContextDataProviderMixin, StudentListMixin, ListView):
    login_url = "/admin/login/"
    model = Student
    template_name = 'capstone_proposal.html' 

    def get_queryset(self):
        queryset = super(CapstoneProposalView, self).get_queryset()
        return queryset.filter(internship__status=3, capstone__status=0) 


class CapstonePartOneView(LoginRequiredMixin, ContextDataProviderMixin, StudentListMixin, ListView):
    login_url = "/admin/login/"
    model = Student
    template_name = 'capstone_part_one.html' 

    def get_queryset(self):
        queryset = super(CapstonePartOneView, self).get_queryset()
        return queryset.filter(capstone__isnull=False, capstone__status=1) 


class CapstonePartTwoView(LoginRequiredMixin, ContextDataProviderMixin, StudentListMixin, ListView):
    login_url = "/admin/login/"
    model = Student
    template_name = 'capstone_part_two.html' 

    def get_queryset(self):
        queryset = super(CapstonePartTwoView, self).get_queryset()
        return queryset.filter(capstone__isnull=False, capstone__status=2) 

class CapstoneVivaView(LoginRequiredMixin, ContextDataProviderMixin, StudentListMixin, ListView):
    login_url = "/admin/login/"
    model = Student
    template_name = 'capstone_viva.html' 

class CapstoneCompletionListView(LoginRequiredMixin, ContextDataProviderMixin, StudentListMixin, ListView):
    login_url = "/admin/login/"
    model = Student
    template_name = 'capstone_completion_list.html' 


class StudentActivitiesView(LoginRequiredMixin, GroupRequiredMixin, ContextDataProviderMixin, ListView):
    login_url = "/student/login/"
    model = Activity
    template_name = 'student_activities.html' 
    group_required = u"student group"
    raise_exception = True

class StudentProfileView(LoginRequiredMixin, GroupRequiredMixin, ContextDataProviderMixin, TemplateView):
    login_url = "/student/login/"
    template_name = 'student_profile.html' 
    group_required = u"student group"
    raise_exception = True

class ScadiilAboutView(LoginRequiredMixin, GroupRequiredMixin, ContextDataProviderMixin, ListView):
    login_url = "/student/login/"
    model = Activity
    template_name = 'scadiil_about.html' 
    group_required = u"student group"
    raise_exception = True
