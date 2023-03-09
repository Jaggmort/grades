import django
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Lesson
from datacenter.models import Commendation
from datacenter.models import Schoolkid
from django.shortcuts import get_object_or_404


def fix_marks(schoolkid):
    marks = Mark.objects.filter(schoolkid__in=schoolkid, points__in=[2, 3])
    for mark in marks:
        mark.points = 5
        mark.save()


def remove_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid__in=schoolkid)
    chastisements.delete()


def create_commendation(schoolkid, subject):
    try:
        cls = get_object_or_404(Schoolkid, full_name__contains=schoolkid)
    except django.http.response.Http404:
        print('Ученики с таким именем не найдены')
        return
    except Schoolkid.MultipleObjectsReturned:
        print('Найдено несколько учеников')
        return
    lesson = Lesson.objects.filter(year_of_study=cls.year_of_study,
                                   group_letter=cls.group_letter,
                                   subject__title=subject
                                   ).last()
    commendation = Commendation(text='123',
                                created=lesson.date,
                                schoolkid=cls,
                                subject=lesson.subject,
                                teacher=lesson.teacher
                                )
    commendation.save()