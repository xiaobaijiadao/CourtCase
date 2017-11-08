from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Case

from . import docs

def index(request):
    test = docs.Test(name = 'linux')
    test.save()
    print(docs.Test.objects())
    return render(request, 'recommend/index.html')

def list_format(cs):
    cases=[]
    for c in cs:
        case = dict(
            id = c.id,
            title = c.title,
        )
        cases.append(c)
    return cases

def list(request):
	result = {}
	limit = 6
	key = str(request.GET.get('key'))

	cs = Case.objects.filter(keyWords__icontains = key).order_by('id')
	pre_cases = list_format(cs)

	paginator = Paginator(pre_cases, limit)

	page = request.GET.get('page', 1)
	print(key, page)
	try:
		cases = paginator.page(page)
	except PageNotAnInteger:
		cases = paginator.page(1)
	except EmptyPage:
		cases = paginator.page(paginator.num_pages)

	result['cases'] = cases
	result['cases_num'] = len(cases)
	result['isPaging'] = len(pre_cases)>6
	result['key'] = key

	print(result)

	return render(request, 'recommend/list.html', result)

def display(request , case_id):
	result = {}

	case = Case.objects.get(id=case_id)

	result['case'] = dict(
		id = case.id,
		title = case.title,
		keywords = case.keyWords,
		content = case.content, 
	)

	return render(request, 'recommend/display.html', result)

def dafen():
	return 

def sort():
	return