from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .docs import Dao
from .roughExtract import roughExtract
from .fineExtract import fineExtract
from .point import point

db = Dao()

def index(request):
    return render(request, 'recommend/index.html')


def list_format(cases):
    res = []

    db.getCollection('caseTest', 'cases')

    for case in cases:
        c = db.findByKey("_id", case[0])
        res.append(dict(
            id=c["_id"],
            title=c["title"]
        ))

    return res


def list(request):
    result = {}
    limit = 6
    query = str(request.GET.get('key'))

    print("enter rough")
    roughRes = roughExtract(query).getIndexList()
    print(roughRes)
    print("enter fine")
    fineRes = fineExtract(query, roughRes).getResult()
    print(fineRes)
    print("enter point")
    pointRes = point(fineRes).getRes()
    print(pointRes)

    #    cs = Case.objects.filter(keyWords__icontains=key).order_by('id')
    pre_cases = list_format(pointRes)

    paginator = Paginator(pre_cases, limit)

    page = request.GET.get('page', 1)
    print(query, page)
    try:
        cases = paginator.page(page)
    except PageNotAnInteger:
        cases = paginator.page(1)
    except EmptyPage:
        cases = paginator.page(paginator.num_pages)

    result['cases'] = cases
    result['cases_num'] = len(cases)
    result['isPaging'] = len(pre_cases) > 6
    result['key'] = query

    print(result)

    return render(request, 'recommend/list.html', result)


def display(request, case_id):
    result = {}

    db.getCollection('caseTest', 'cases')
    case = db.findByKey("_id", case_id)
#    case = Case.objects.get(id=case_id)

    result['case'] = dict(
        id=case["_id"],
        title=case["title"],
        # keywords=case.keyWords,
        # content=case.content,
    )

    return render(request, 'recommend/display.html', result)
