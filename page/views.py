from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from base.models import EducationalYear
from page.models import OfferedCourse, TERM


def get_all_term_year():
    year_term_list = []
    for year in EducationalYear.objects.all().order_by('-year'):
        for term in reversed(list(TERM)):
            y = year.year
            t = term[0]
            s = 0
            for o in OfferedCourse.objects.filter(year=year, term=t):
                s += o.page.count()
            year_term_list.append({
                'year': y,
                'term': term,
                'count': s,
            })
    return year_term_list


@login_required
def all_term_year(request):
    return render(
        request,
        'page/all_year_term.html',
        {
            'year_term_list': get_all_term_year(),
        })


@login_required
def term_year(request, year_num, term_num):
    offered_courses = OfferedCourse.objects.filter(year__year=year_num, term=term_num).exclude(page=None)
    return render(
        request,
        'page/year_term.html',
        {
            'offered_courses': offered_courses,
            'year_term_list': get_all_term_year(),
            'year': year_num,
            'term': list(TERM)[int(term_num) - 1],
        })


@login_required
def course(request, year_num, term_num, course_num, group_num):
    offered_course = get_object_or_404(OfferedCourse,
                                       course__course_number=course_num,
                                       group_number=group_num,
                                       term=term_num,
                                       year__year=year_num)
    p = offered_course.page.last()
    return render(
        request,
        'page/course_page.html',
        {
            'offered_course': offered_course,
            'course_page': p,
        })