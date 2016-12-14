from django import template
import datetime

register = template.Library()

def human_date(value):
    now = datetime.datetime.now()
    num_days = value-now.date()
    num_days = num_days.days

    if num_days==0:
        return "today"

    elif num_days<0:
        if num_days==-1:
            return str(abs(num_days)) + " day ago"
        return str(abs(num_days)) + " days ago"

    else:
        if num_days==1:
            return str(abs(num_days)) + " day more"
        return str(abs(num_days)) + " days more"
    return value

def past_count(object_list):
    count = 0
    for objet in object_list:
        if objet.date < datetime.date.today():
            count = count + 1
        if objet.date == datetime.date.today() and \
                objet.time < datetime.datetime.now().time():
            count = count + 1
    return count

def upcoming_count(object_list):
    count = 0
    for objet in object_list:
        if objet.date > datetime.date.today():
            count = count + 1
        if objet.date == datetime.date.today() and \
                objet.time > datetime.datetime.now().time():
            count = count + 1
    return count

def hottize(object_list, days):
    count = 0
    for objet in object_list:
        days_diff = objet.date - datetime.date.today()
        days_diff = days_diff.days
        if  days_diff == days or days_diff < days and \
                days_diff > 0:
            count = count + 1
    return count



register.filter('human_date', human_date)
register.filter('past_count', past_count)
register.filter('upcoming_count', upcoming_count)
register.filter('hottize', hottize)


