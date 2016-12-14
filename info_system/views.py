from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.db import IntegrityError
from django.conf import settings
from django.views.generic.edit import FormView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic import View
from django.views.generic import TemplateView
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.db.models import Count

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from braces.views import LoginRequiredMixin, GroupRequiredMixin

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template import loader
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.core.urlresolvers import reverse

from forms import StudentForm, UploadForm
from forms import StudentLoginForm, NewActivityForm
from forms import NewSeminarForm, EnrolStudentForm
from models import * 
from util import excel_reader

from datetime import datetime
import os

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
        upcoming_count = self.upcoming_count(Activity.objects.all()) 

        if self.role == 'admin':
            navbar_admin = 'navbar-admin'
            navbar_admin_brand = 'navbar-admin-brand'
            title   = 'SCADIIL ADMIN'
            logout  = 'admin:logout'

        context["navbar_admin"] = navbar_admin
        context["navbar_admin_brand"] = navbar_admin_brand
        context["title"]  = title
        context["logout"] = logout
        context["today"] = datetime.now()
        context["upcoming_activities_count"] = upcoming_count 
        return context

    def upcoming_count(self, object_list):
        import datetime
        count = 0
        for objet in object_list:
            if objet.date > datetime.date.today():
                count = count + 1
            if objet.date == datetime.date.today() and \
                    objet.time > datetime.datetime.now().time():
                count = count + 1
        return count

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

class EnrolStudentView(ContextDataProviderMixin, FormView):

    def form_valid(self, form):
        # create a user object from form info
        try:
            user = User.objects.create_user(first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['surname'],
                        username=form.cleaned_data['id_number'].upper(),
                        email=form.cleaned_data['email_address'],
                        password=form.cleaned_data['surname']+"123")
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
            return super(EnrolStudentView, self).form_invalid(form)

        # create the student object
        student = Student(user=user, middle_name=form.cleaned_data['middle_name'],
                          phone_number=form.cleaned_data['phone_number'],
                          program=form.cleaned_data['program'])
        student.save()
        return super(EnrolStudentView, self).form_valid(form)

    def form_invalid(self, form):
        print "form not valid" 
        messages.error(self.request, 'There are issues with your form! Please correct them.')
        return super(EnrolStudentView, self).form_invalid(form)


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

class StudentDetailsView(LoginRequiredMixin, ContextDataProviderMixin, DetailView):
    login_url = "/admin/login/"
    model = Student
    template_name = 'student_details.html' 

class ScadiilCompletionView(LoginRequiredMixin, ContextDataProviderMixin, StudentListMixin, ListView):
    login_url = "/admin/login/"
    model = Student
    template_name = 'scadiil_completion_list.html' 

    def get_queryset(self):
        queryset = super(ScadiilCompletionView, self).get_queryset()
        return queryset.annotate(sem_att=Count('seminarattendance')).\
                                       filter(capstone__status=3, internship__status=3,sem_att__gte=12) 

class AdminActivitiesView(LoginRequiredMixin, GroupRequiredMixin, ContextDataProviderMixin, ListView):
    login_url = "/admin/login/"
    model = Activity
    template_name = 'activities.html' 
    group_required = u"managers"
    raise_exception = True

class ActivityDetailsView(LoginRequiredMixin, ContextDataProviderMixin, DetailView):
    login_url = "/admin/login/"
    model = Activity
    template_name = 'activity_details.html' 

class NewActivitiesView(LoginRequiredMixin, ContextDataProviderMixin, FormView):
    login_url = "/admin/login/"
    form_class = NewActivityForm
    template_name = 'activity_new.html' 
    success_url = './'

    def form_valid(self, form):
        target_str = ''
        for target in self.request.POST.getlist('targets[]'):
            target_str = target_str + target + ','

        new_activity = Activity(title=form.cleaned_data['title'],
                                description=form.cleaned_data['description'],
                                date=form.cleaned_data['date'],
                                time=form.cleaned_data['time'],
                                target_school=form.cleaned_data['school'],
                                target_groups=target_str)
        new_activity.save()
        return super(NewActivitiesView, self).form_valid(form)

    def form_invalid(self, form):
        print "invalid form submitted"
        return super(NewActivitiesView, self).form_invalid(form)

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

class UFSNewGrade(LoginRequiredMixin, ContextDataProviderMixin, FormView):
    login_url = "/admin/login/"
    form_class = UploadForm
    template_name = 'ufs_new.html' 
    success_url   = './new/review'

    def form_valid(self, form):
        in_file = self.request.FILES['file']
        in_file_name = in_file.name
        util_dir = os.path.join(settings.BASE_DIR, "util")
        out_file_name = os.path.join(util_dir, in_file_name)

        with open(out_file_name, 'wb+') as destination:
            for chunk in in_file.chunks():
                destination.write(chunk)

        grades = excel_reader.read_grade_sheet(out_file_name)
        self.request.session['grades'] = grades
        return super(UFSNewGrade, self).form_valid(form)

    def form_invalid(self, form):
        print "form has some errors"
        print form.errors
        return super(UFSNewGrade, self).form_invalid(form)


class CDESView(LoginRequiredMixin, ContextDataProviderMixin, StudentListMixin, ListView):
    login_url = "/admin/login/"
    model = Student
    template_name = 'cdes_list.html' 

    def get_queryset(self):
        queryset = super(CDESView, self).get_queryset()
        return queryset.filter(CDES_passed=True) 

class CDESNewGrade(LoginRequiredMixin, ContextDataProviderMixin, FormView):
    form_class = UploadForm
    template_name = 'cdes_new.html' 
    success_url   = './new/review'

    def form_valid(self, form):
        in_file = self.request.FILES['file']
        in_file_name = in_file.name
        util_dir = os.path.join(settings.BASE_DIR, "util")
        out_file_name = os.path.join(util_dir, in_file_name)

        with open(out_file_name, 'wb+') as destination:
            for chunk in in_file.chunks():
                destination.write(chunk)

        grades = excel_reader.read_grade_sheet(out_file_name)
        self.request.session['grades'] = grades

        return super(CDESNewGrade, self).form_valid(form)

    def form_invalid(self, form):
        print "form has some errors"
        return super(CDESNewGrade, self).form_invalid(form)

class GradeListView(LoginRequiredMixin, ContextDataProviderMixin, TemplateView):
    login_url = "/admin/login/"
    template_name = 'grade_list.html' 
    course = None

    def get_context_data(self, **kwargs):
        context = super(GradeListView, 
                        self).get_context_data(**kwargs)
        grades = self.request.session['grades']
        fail = 0

        for value in grades.itervalues():
            if value[2] < 60 or value[2] == "i" or value[2] == "I":
                fail = fail + 1

        context['grades'] = grades
        context['course'] = self.course
        context['total'] = len(grades) 
        context['fail'] = fail 
        context['pass'] = len(grades)-fail
        return context

class SaveGrade(LoginRequiredMixin, ContextDataProviderMixin, View):
    login_url = "/admin/login/"
    course = None

    def get(self, request, *args, **kwargs):
        grades = self.request.session['grades']

        if self.course == 'ufs':
            for value in grades.itervalues():  
                if value[2] < 60 or value[2] == "i" or value[2] == "I":
                    continue
                try:
                    user = User.objects.get(username=value[1])
                    student = user.student
                    student.UFS_passed = True
                    student.save()
                except User.DoesNotExist:
                    print value[1]
                    pass
            self.request.session.pop('grades')
            return redirect("admin:courses-ufs")

        if self.course == 'cdes':
            for value in grades.itervalues():  
                if value[2] < 60 or value[2] == "i" or value[2] == "I":
                    continue
                try:
                    user = User.objects.get(username=value[1])
                    student = user.student
                    student.CDES_passed = True
                    student.save()
                except User.DoesNotExist:
                    print value[1]
                    pass
            self.request.session.pop('grades')
            return redirect("admin:courses-cdes")
        return redirect("admin:activities")

class PreInternStudentView(LoginRequiredMixin, ContextDataProviderMixin, StudentListMixin, ListView):
    login_url = "/admin/login/"
    model = Student
    template_name = 'internship_pre.html' 

    def get_queryset(self):
        queryset = super(PreInternStudentView, self).get_queryset()
        return queryset.annotate(sem_attendance=Count('seminarattendance')).\
             filter(CDES_passed=True, UFS_passed=True, sem_attendance__gte=1) 


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
        context["sates_count"] = queryset.filter(school=1).count() 
        context["asdass_count"] = queryset.filter(school=3).count() 
        context["abs_count"] = queryset.filter(school=2).count() 
        return context

class NewSeminarAttendanceView(LoginRequiredMixin, ContextDataProviderMixin, FormView):
    login_url = "/admin/login/"
    form_class = UploadForm
    template_name = 'upload_seminar_attendance.html' 
    success_url = './new/review'

    def form_valid(self, form):
        in_file = self.request.FILES['file']
        in_file_name = in_file.name
        util_dir = os.path.join(settings.BASE_DIR, "util")
        out_file_name = os.path.join(util_dir, in_file_name)

        with open(out_file_name, 'wb+') as destination:
            for chunk in in_file.chunks():
                destination.write(chunk)

        attendance_data = excel_reader.read_attendance_sheet(out_file_name)
        self.request.session['attendance'] = attendance_data
        return super(NewSeminarAttendanceView, self).form_valid(form)

    def form_invalid(self, form):
        print "form has some errors"
        print form.errors
        return super(NewSeminarAttendanceView, self).form_invalid(form)

class EditSeminarView(LoginRequiredMixin, ContextDataProviderMixin, UpdateView):
    login_url = "/admin/login/"
    template_name = 'seminar_new.html' 

    def get_context_data(self, **kwargs):
        from django.forms.models import model_to_dict
        self.object = None
        context = super(EditSeminarView, 
                        self).get_context_data(**kwargs)
        seminar = Seminar.objects.get(pk=kwargs['pk'])  
        seminar_form = NewSeminarForm(initial=model_to_dict(seminar))

        context['form'] = seminar_form
        context['heading'] = "Edit This Seminar" 
        context['button_text'] = "Save Changes" 
        return context

    def get(self, request, *args, **kwargs):
        self.object = None
        return render(request, self.template_name, self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        self.object = None
        form = NewSeminarForm(request.POST)

        if form.is_valid():
            seminar = Seminar.objects.get(pk=kwargs['pk'])  
            seminar.title=form.cleaned_data['title']
            seminar.speaker=form.cleaned_data['speaker']
            seminar.description=form.cleaned_data['description']
            seminar.date=form.cleaned_data['date']
            seminar.time=form.cleaned_data['time']
            seminar.school=form.cleaned_data['school']

            activity = seminar.activity
            activity.title='USS -- ' + form.cleaned_data['title']
            activity.description=form.cleaned_data['description']
            activity.date=form.cleaned_data['date']
            activity.time=form.cleaned_data['time']
            activity.target_school=form.cleaned_data['school']
            activity.target_groups="0,1"

            activity.save()
            seminar.save()
            return HttpResponseRedirect('../../details/' + kwargs['pk'])
        print form.errors

        return render(request, self.template_name, self.get_context_data(**kwargs))

class AttendanceListView(LoginRequiredMixin, ContextDataProviderMixin, TemplateView):
    login_url = "/admin/login/"
    template_name = 'attendance_list.html' 

    def get_context_data(self, **kwargs):
        context = super(AttendanceListView, 
                        self).get_context_data(**kwargs)
        attendance = self.request.session['attendance']

        context['attendance'] = attendance 
        context['total'] = len(attendance) 
        return context

class SaveAttendanceView(LoginRequiredMixin, ContextDataProviderMixin, View):
    login_url = "/admin/login/"

    def get(self, request, *args, **kwargs):
        attendance = self.request.session['attendance']
        seminar = get_object_or_404(Seminar, pk=kwargs['pk'])
        unavailable_ids = []

        for value in attendance.itervalues():
            try:
                student_user = User.objects.get(username=value[1])
                student = student_user.student
                manager = self.request.user.manager
                seminar_attendance = SeminarAttendance(student=student,
                                                       authorized_by=manager, 
                                                       seminar=seminar)
                seminar_attendance.save()
            except User.DoesNotExist:
                unavailable_ids.append(value[1])
                continue
        return redirect("admin:activities")

class SeminarNewView(LoginRequiredMixin, ContextDataProviderMixin, FormView):
    form_class = NewSeminarForm
    template_name = 'seminar_new.html' 
    success_url   = '../all'

    def get_context_data(self, **kwargs):
        context = super(SeminarNewView, 
                        self).get_context_data(**kwargs)

        context['heading'] = "Create New Seminar" 
        context['button_text'] = "Create This Seminar" 
        return context

    def form_valid(self, form):
        new_activity = Activity(title='USS--' + form.cleaned_data['title'],
                                description=form.cleaned_data['description'],
                                date=form.cleaned_data['date'],
                                time=form.cleaned_data['time'],
                                target_school=form.cleaned_data['school'],
                                target_groups="0,1")
        new_activity.save()

        new_seminar = Seminar(title=form.cleaned_data['title'],
                              speaker=form.cleaned_data['speaker'],
                              description=form.cleaned_data['description'],
                              date=form.cleaned_data['date'],
                              time=form.cleaned_data['time'],
                              school=form.cleaned_data['school'],
                              activity=new_activity)
        new_seminar.save()

        return super(SeminarNewView, self).form_valid(form)


    def form_invalid(self, form):
        print "form has some errors"
        return super(SeminarNewView, self).form_invalid(form)


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
        context["sates_count"] = queryset.filter(school=1).count() 
        context["asdass_count"] = queryset.filter(school=3).count() 
        context["abs_count"] = queryset.filter(school=2).count() 
        return context

class DetailSeminarView(LoginRequiredMixin, ContextDataProviderMixin, DetailView):
    login_url = "/admin/login/"
    model = Seminar
    template_name = 'seminar_details.html' 

    def get_context_data(self, **kwargs):
        context = super(DetailSeminarView, 
                        self).get_context_data(**kwargs)
        total_attendance = self.object.seminarattendance_set.all().count()
        context["attendance_count"] = total_attendance
        return context

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

    def get_queryset(self):
        queryset = super(StudentActivitiesView, self).get_queryset()
        student_prog = self.request.user.student.program 
        return queryset.filter(target_school=student_prog).order_by('-date')

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
