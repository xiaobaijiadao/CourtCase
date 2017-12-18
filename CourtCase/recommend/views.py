from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .collections import paragraph, lawcase
from .roughExtract import roughExtract
from time import clock


def index(request):
    return render(request, 'recommend/index.html')


def list_format(cases):
    res = []

    par = paragraph()

    for case in cases:
        c = par.getInfo(case)
        res.append(dict(
            id=str(c["_id"]),
            title=c["title"]
        ))

    return res


def list(request):
    result = {}
    limit = 8
    query = str(request.GET.get('key'))

    print("enter rough")
    startSeg = clock()
    roughRes = roughExtract(query).getIndexList2()
    finishSeg = clock()
    print("索引耗时： %d 微秒" % (finishSeg - startSeg))
    # print(roughRes)
    # print("enter fine")
    # fineRes = fineExtract(query, roughRes).getResult()
    # print(fineRes)
    # print("enter point")
    # pointRes = point(roughRes).getRes()
    # pointRes = point(fineRes).getRes()
    # print(pointRes)
    pointRes = roughRes

    #    cs = Case.objects.filter(keyWords__icontains=key).order_by('id')
    startPage = clock()
    pre_cases = list_format(pointRes)

    paginator = Paginator(pre_cases, limit)

    page = request.GET.get('page', 1)

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
    finishPage = clock()
    print("分页耗时： %d 微秒" % (finishPage - startPage))

    return render(request, 'recommend/list.html', result)


def display(request, case_id):
    result = {}
    par = paragraph()
    lc = lawcase()

    case = par.getInfo(case_id)
    info = lc.getInfo(case["fullTextId"])

    result['case'] = dict(
        id=case["_id"],
        title=case["title"],
        content = info,
    )

    return render(request, 'recommend/display.html', result)
