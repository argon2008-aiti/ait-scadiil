from django.db import models
from django.contrib.auth.models import User


SCHOOL = [
    (1, "SATES (Engineering)"),
    (2, "ABS (Business)"),
    (3, "ASDASS (IT/Computer Science)")
]

SEMESTER = [
    (1, "First"),
    (2, "Second")
]

CAPSTONE_STATUS = [
    (-1,"NOT STARTED"), 
    (0, "PROPOSAL"),
    (1, "PART ONE"),
    (2, "PART TWO"),
    (3, "COMPLETED"),
]

INTERNSHIP_STATUS = [
    (-1,"NOT STARTED"), 
    (0, "PREPARATION"),
    (1, "AT POST"),
    (2, "RETURNEE"),
    (3, "COMPLETED"),
]

class Supervisor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)

class CapstoneProject(models.Model):
    title  = models.CharField(max_length=200)
    status = models.IntegerField(default=-1, choices=CAPSTONE_STATUS)
    part_one_mark = models.FloatField()
    part_two_mark = models.FloatField()
    supervisor = models.ForeignKey(Supervisor)

    def __unicode__(self):
        return self.title


class Internship(models.Model):
    company = models.CharField(max_length=100)
    date_started = models.DateField()
    date_ended   = models.DateField()
    status  = models.IntegerField(default=-1, choices=INTERNSHIP_STATUS)

    def __unicode__(self):
        return self.company


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    middle_name = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=20)
    CDES_passed = models.BooleanField(default=False)
    UFS_passed = models.BooleanField(default=False)
    capstone   = models.ForeignKey(CapstoneProject, null=True, blank=True)
    internship = models.ForeignKey(Internship, null=True, blank=True)
    scadiil_level = models.IntegerField(default=0)
    program = models.IntegerField(choices=SCHOOL)

    def __unicode__(self):
        return self.user.first_name +" "+ self.user.last_name + "(" + self.user.username + ")"

    def get_seminar_attendance(self):
        return len(self.seminarattendance_set.all())


class Manager(models.Model):
    user = models.OneToOneField(User)
    middle_name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.user.first_name +" "+ self.user.last_name


class Seminar(models.Model):
    title = models.CharField(max_length=300) 
    speaker = models.CharField(max_length=200)
    description = models.TextField()
    date  = models.DateField()
    time  = models.TimeField()
    academic_year = models.CharField(max_length=20)
    semester = models.IntegerField(choices=SEMESTER)
    school = models.IntegerField(choices=SCHOOL)

    def __unicode__(self):
        return self.title + ":" + self.speaker

class Activity(models.Model):
    title = models.CharField(max_length=300)
    date  = models.DateField()
    time  = models.TimeField()
    description = models.TextField()
    target_school = models.IntegerField(default=3)
    target_groups = models.CharField(max_length=50)
    send_reminder = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title + "--" + self.date + "--" + self.time 

class Message(models.Model):
    subject = models.CharField(max_length=300)
    content = models.TextField()
    datetime_stamp = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.subject 

class MessageScheduler(models.Model):
    message = models.ForeignKey(Message)
    sch_date = models.DateField()
    sch_time = models.TimeField()

    def __unicode__(self):
        return self.subject + "--" + self.sch_date

class SeminarAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE) 
    seminar = models.ForeignKey(Seminar, on_delete=models.CASCADE)
    date    = models.DateField(auto_now_add=True)
    time    = models.TimeField(auto_now_add=True)
    authorized_by = models.ForeignKey(Manager)

    def __unicode__(self):
        return self.student.username + "--" + self.seminar.title

