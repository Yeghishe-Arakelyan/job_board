from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Job, Category
from .forms import QuantityForm



def paginat(request, list_objects):
	p = Paginator(list_objects, 20)
	page_number = request.GET.get('page')
	try:
		page_obj = p.get_page(page_number)
	except PageNotAnInteger:
		page_obj = p.page(1)
	except EmptyPage:
		page_obj = p.page(p.num_pages)
	return page_obj


def home_page(request):
	jobs = Job.objects.all()
	categories = Category.objects.all()
	context = {'jobs': paginat(request ,jobs),
	    'categories': categories,}
	return render(request, 'home_page.html', context)


def search(request):
	query = request.GET.get('q')
	jobs = Job.objects.filter(title__icontains=query).all()
	categories = Category.objects.all()
	context = {'jobs': paginat(request ,jobs),
	    'categories': categories,}
	return render(request, 'home_page.html', context)


def filter_by_category(request, slug):
    
    category = Category.objects.filter(slug=slug).first()
    jobs = Job.objects.filter(category=category)
    categories = Category.objects.all()
    context = {'jobs': paginat(request, jobs),
	     'categories': categories,  }
    return render(request, 'home_page.html', context)

def job_detail(request, slug):
    form = QuantityForm()
    categories = Category.objects.all()
    job = get_object_or_404(Job, slug=slug)
    related_jobs = Job.objects.filter(category=job.category).all()[:5]
    context = {
        'title': job.title,
        'job': job,
        'form': form,
        'related_jobs': related_jobs,
		'categories': categories,
    }
    return render(request, 'job_detail.html', context)


