from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

from time import clock
import pymongo, json

from .collections import paragraph, lawcase, searchPerformTest
from .casePerform import casePerform
from .statutePerform import statutePerform
from .roughExtract import roughExtract

TACTICS_OPTIONS = ["关键字", "TFIDF", "LDA"]


def index(request):
    return render(request, 'recommend/index.html')


def list_format(cases, option):
    res = []
    par = paragraph()

    if option == "LDA":
        for case in cases:
            c = par.getInfoByFullTextId(case)
            res.append(dict(
                id=str(c[0]),
                title=c[1],
            ))
    else:
        for case in cases:
            c = par.getInfo(case)
            res.append(dict(
                id=str(c[0]),
                title=c[1],
            ))

    return res


def list(request):
    result = {}
    page_limit = 10
    query = str(request.GET.get('key'))
    option = str(request.GET.get('option'))
    print(option)

    print("enter rough")
    startSeg = clock()
    roughRes = None

    if option == '关键字':
        roughRes = roughExtract(query).getIndexListbykeyword()
    elif option == 'TFIDF':
        roughRes = roughExtract(query).getIndexListbytfidf()
    elif option == 'LDA':
        roughRes = roughExtract(query).getIndexListbyLda()
    else:
        roughRes = roughExtract(query).getIndexListbykeyword()

    finishSeg = clock()
    print("索引耗时： %d 微秒" % (finishSeg - startSeg))
    # print(roughRes)
    # print("enter point")
    # pointRes = point(roughRes).getRes()
    # print(pointRes)
    pointRes = roughRes

    startPage = clock()
    pre_cases = list_format(pointRes, option)

    paginator = Paginator(pre_cases, page_limit)

    page = request.GET.get('page', 1)

    try:
        cases = paginator.page(page)
    except PageNotAnInteger:
        cases = paginator.page(1)
    except EmptyPage:
        cases = paginator.page(paginator.num_pages)

    result['query'] = query
    result['tactics_option'] = TACTICS_OPTIONS
    result['option'] = option
    result['cases'] = cases
    result['cases_num'] = len(cases)
    result['isPaging'] = len(pre_cases) > 6
    result['key'] = query
    finishPage = clock()
    print("分页耗时： %d 微秒" % (finishPage - startPage))

    return render(request, 'recommend/list.html', result)


def display(request, case_id):
    print(case_id)
    result = {}
    par = paragraph()
    lc = lawcase()

    case = par.getInfoByFullTextId(case_id)
    text = lc.getInfo(case_id)

    result['case'] = dict(
        title=case[1],
        content=text,
    )

    return render(request, 'recommend/display.html', result)


def getcoverCount(standard, test):
    count = 0
    for item in test:
        if item in standard:
            count += 1
    return count


def gettestresult(searchRes, option, col, referenceStandard):
    idlist = [r['id'] for r in list_format(searchRes, option)]
    result = []
    for id in idlist:
        case = dict()
        case['id'] = id
        reference = [ref['name'].strip() + ref['levelone'].strip() \
                     for ref in col.find_one({"fullTextId": id})['references']]
        case['ref'] = reference
        case['covercount'] = getcoverCount(referenceStandard, reference)
        result.append(case)
    return result


def test(request, pwd, option):
    if pwd == "p123456":
        print("enter test************")
        col1 = settings.DB_CON.divorceCase.lawcase
        col2 = settings.DB_CON.divorceCase.lawreference
        col3 = settings.DB_CON.divorceCase.searchPerformTest if option == '3' else settings.DB_CON.divorceCase.searchPerformVerify

        i = 1

        cur = col1.find({"tag": option}, no_cursor_timeout=True)
        for case in cur:
            referenceStandard = [ref['name'].strip() + ref['levelone'].strip() \
                                 for ref in col2.find_one({"fullTextId": case['fullTextId']})['references']]

            res = dict()
            res['searchId'] = case['fullTextId']
            res['ref'] = referenceStandard

            query = case['plaintiffAlleges']['text'] \
                    + case['defendantArgued']['text'] \
                    + case['factFound']['text']
            rough = roughExtract(query)

            roughResByKeyword = rough.getIndexListbykeyword()
            res['resByKeyWord'] = gettestresult(roughResByKeyword, "关键字", col2, referenceStandard)

            roughResByTfidf = rough.getIndexListbytfidf()
            res['resByTfidf'] = gettestresult(roughResByTfidf, "TFIDF", col2, referenceStandard)

            roughResByLda = rough.getIndexListbyLda()
            res['resByLda'] = gettestresult(roughResByLda, "LDA", col2, referenceStandard)

            col3.insert(res)
            print("第 %d 次写入" % i)
            i += 1
        cur.close()
        print('finish!')
    else:
        return HttpResponse("faild!")


def genEvaluate(request, pwd):
    if pwd == "p123456":
        col = settings.DB_CON.divorceCase.searchEvaluate
        resList = []

        sp = searchPerformTest()
        statuteEvaluate = statutePerform(sp).genEvaluate()
        resList.append({
            'name' : 'statutePrecison',
            'method' : statuteEvaluate['precision']
        })
        resList.append({
            'name': 'statuteRecall',
            'method': statuteEvaluate['recall']
        })
        resList.append({
            'name': 'statuteF1',
            'method': statuteEvaluate['f1']
        })

        caseEvaluate = casePerform(sp).genEvaluate()
        resList.append({
            'name': 'casePrecision',
            'method': caseEvaluate['precision'],
        })

        col.insert(resList)

        return True
    else:
        return HttpResponse('faild!')



def test_res_display(request):
    sp = searchPerformTest()
    res = statutePerform(sp).getStatutePerform(0)
    return render(request, 'recommend/testResult.html', res)


def case_p_display(request):
    sp = searchPerformTest()
    res = casePerform(sp).getCasePerform()
    return JsonResponse(res)


def statute_p_display(request):
    sp = searchPerformTest()
    res = statutePerform(sp).getStatutePerform(0)
    return JsonResponse(res)


def statute_r_display(request):
    sp = searchPerformTest()
    res = statutePerform(sp).getStatutePerform(1)
    return JsonResponse(res)


def statute_p_r_display(request):
    sp = searchPerformTest()
    res = statutePerform(sp).getStatutePerform(2)
    return JsonResponse(res)
