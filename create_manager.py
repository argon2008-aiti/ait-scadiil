from django.conf import settings
import django

import sys
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ait_ilcdmp.settings")
django.setup()

from django.contrib.auth.models import User, Group
from django.db import IntegrityError
from info_system.models import Manager

first_name = sys.argv[1]
last_name  = sys.argv[2]
username   = sys.argv[3]
email      = sys.argv[4]
password   = username + "123"

print "Creating new manager object for " + first_name + " " + last_name
try:
    user = User.objects.create_user(username=username, last_name=last_name, email=email, \
                first_name=first_name, password=password)

except IntegrityError as e:
    print "The username you provided already exists. Aborting..."
    sys.exit()

manager_group, created = Group.objects.get_or_create(name="managers")

manager = Manager(user=user, middle_name=" ")
manager.save()

user.groups.add(manager_group)
user.save()

